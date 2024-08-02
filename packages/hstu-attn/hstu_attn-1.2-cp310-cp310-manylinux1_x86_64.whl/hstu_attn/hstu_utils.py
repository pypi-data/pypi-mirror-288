import torch
from typing import Callable, Dict, List, Optional, Tuple, NamedTuple, Union
import abc
import torch.nn.functional as F
import torch.nn as nn
import fbgemm_gpu

import time


class Timer:
    def __init__(self):
        self._start = torch.cuda.Event(enable_timing=True)
        self._end = torch.cuda.Event(enable_timing=True)

    def start(self):
        """start timing"""
        self._start.record()

    def stop(self, str):
        """stop timing and print ret"""
        self._end.record()
        torch.cuda.synchronize()
        elapsed = self._start.elapsed_time(self._end)
        print(str + " exctuted time is {} ms".format(elapsed))

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


class RelativeAttentionBiasModule(torch.nn.Module):

    @abc.abstractmethod
    def forward(
        self,
        all_timestamps: torch.Tensor,
    ) -> torch.Tensor:
        """
        Args:
            all_timestamps: [B, N] x int64
        Returns:
            torch.float tensor broadcastable to [B, N, N]
        """
        pass


class RelativeBucketedTimeAndPositionBasedBias(RelativeAttentionBiasModule):
    """
    Bucketizes timespans based on ts(next-item) - ts(current-item).
    """

    def __init__(
        self,
        max_seq_len: int,
        num_buckets: int,
        bucketization_fn: Callable[[torch.Tensor], torch.Tensor],
    ) -> None:
        super().__init__()

        self._max_seq_len: int = max_seq_len
        self._ts_w = torch.nn.Parameter(
            torch.empty(num_buckets + 1).normal_(mean=0, std=0.02),
        )
        self._pos_w = torch.nn.Parameter(
            torch.empty(2 * max_seq_len - 1).normal_(mean=0, std=0.02),
        )
        self._num_buckets: int = num_buckets
        self._bucketization_fn: Callable[[torch.Tensor], torch.Tensor] = bucketization_fn

    def forward(
        self,
        all_timestamps: torch.Tensor,
    ) -> torch.Tensor:
        """
        Args:
            all_timestamps: (B, N).
        Returns:
            (B, N, N).
        """
        B = all_timestamps.size(0)
        N = self._max_seq_len
        t = F.pad(self._pos_w[: 2 * N - 1], [0, N]).repeat(N)
        t = t[..., :-N].reshape(1, N, 3 * N - 2)
        r = (2 * N - 1) // 2

        # [B, N + 1] to simplify tensor manipulations.
        ext_timestamps = torch.cat([all_timestamps, all_timestamps[:, N - 1 : N]], dim=1)
        # causal masking. Otherwise [:, :-1] - [:, 1:] works
        bucketed_timestamps = torch.clamp(
            self._bucketization_fn(
                ext_timestamps[:, 1:].unsqueeze(2) - ext_timestamps[:, :-1].unsqueeze(1)
            ),
            min=0,
            max=self._num_buckets,
        ).detach()
        rel_pos_bias = t[:, :, r:-r]
        rel_ts_bias = torch.index_select(
            self._ts_w, dim=0, index=bucketed_timestamps.view(-1)
        ).view(B, N, N)
        return rel_pos_bias + rel_ts_bias


def _hstu_attention_no_cache(
    num_heads: int,
    attention_dim: int,
    linear_dim: int,
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    x_offsets: torch.Tensor,
    all_timestamps: Optional[torch.Tensor],
    invalid_attn_mask: torch.Tensor,
    rel_attn_bias: RelativeAttentionBiasModule,
    is_causal: bool = True,
):
    torch.backends.cuda.matmul.allow_fp16_reduced_precision_reduction = False
    B: int = x_offsets.size(0) - 1
    n: int = invalid_attn_mask.size(-1)
    padded_q = torch.ops.fbgemm.jagged_to_padded_dense(
        values=q, offsets=[x_offsets], max_lengths=[n], padding_value=0.0
    )
    padded_k = torch.ops.fbgemm.jagged_to_padded_dense(
        values=k, offsets=[x_offsets], max_lengths=[n], padding_value=0.0
    )
    padded_v = torch.ops.fbgemm.jagged_to_padded_dense(v, [x_offsets], [n], padding_value=0.0)

    padded_q = padded_q.view(B, n, num_heads, attention_dim)
    padded_k = padded_k.view(B, n, num_heads, attention_dim)
    padded_v = padded_v.view(B, n, num_heads, linear_dim)

    qk_attn_ref = torch.einsum(
        "bnhd,bmhd->bhnm",
        padded_q,
        padded_k,
    )
    qk_attn = torch.bmm(
        padded_q.permute(0, 2, 1, 3).reshape(-1, n, attention_dim),
        padded_k.permute(0, 2, 3, 1).reshape(-1, attention_dim, n),
    )
    qk_attn = qk_attn.reshape(B, num_heads, n, n)
    torch.testing.assert_close(qk_attn, qk_attn_ref)

    if (all_timestamps is not None) and (
        rel_attn_bias is not None
    ):  # test if rel_attn_bias is not None
        qk_attn = qk_attn + rel_attn_bias(all_timestamps).unsqueeze(1)
    qk_attn = F.silu(qk_attn)
    qk_attn = qk_attn / n
    if is_causal:
        invalid_attn_mask = invalid_attn_mask.unsqueeze(0).unsqueeze(0)
        qk_attn = qk_attn * invalid_attn_mask.type(qk_attn.dtype)
    attn_output_ref = torch.einsum(
        "bhnm,bmhd->bnhd",
        qk_attn,
        padded_v,
    )
    attn_output = (
        torch.bmm(
            qk_attn.reshape(-1, n, n), padded_v.permute(0, 2, 1, 3).reshape(-1, n, linear_dim)
        )
        .reshape(B, num_heads, n, linear_dim)
        .permute(0, 2, 1, 3)
    )
    torch.testing.assert_close(attn_output, attn_output_ref)

    attn_output = attn_output.reshape(B, n, num_heads * linear_dim)
    attn_output = torch.ops.fbgemm.dense_to_jagged(attn_output, [x_offsets])[0]
    return attn_output, padded_q, padded_k


def generate_input(
    batch_size: int,
    heads: int,
    max_uih_len: int,
    max_targets: int,
    attn_dim: int,
    hidden_dim: int,
    num_buckets: int,
    bucket_settings: Tuple[str, float, float],
    dtype: torch.dtype,
    weights_dtype: torch.dtype,
):
    lengths = (
        torch.ones((batch_size,), device=torch.device("cuda"), dtype=torch.int32) * max_uih_len
    )
    # lengths = torch.randint(1, max_uih_len + 1, size=(batch_size,), device=torch.device("cuda"))
    num_targets = torch.randint(max_targets + 1, size=(batch_size,), device=torch.device("cuda"))
    lengths = lengths + num_targets

    max_seq_len = max_uih_len + max_targets
    seq_offsets = torch.zeros((batch_size + 1,), dtype=torch.int64, device=torch.device("cuda"))
    seq_offsets[1:] = torch.cumsum(lengths, dim=0)
    seq_offsets = seq_offsets.type(torch.int32)

    L = int(seq_offsets[-1].item())
    q = (
        torch.empty((L, heads, attn_dim), dtype=dtype, device=torch.device("cuda"))
        .uniform_(-0.1, 0.1)
        .requires_grad_()
    )
    k = (
        torch.empty((L, heads, attn_dim), dtype=dtype, device=torch.device("cuda"))
        .uniform_(-0.1, 0.1)
        .requires_grad_()
    )
    v = (
        torch.empty((L, heads, hidden_dim), dtype=dtype, device=torch.device("cuda"))
        .uniform_(-0.1, 0.1)
        .requires_grad_()
    )

    u = (
        torch.empty((L, heads, hidden_dim), dtype=dtype, device=torch.device("cuda"))
        .uniform_(-0.1, 0.1)
        .requires_grad_()
    )

    time_delta = 0.1
    timestamp_deltas: torch.Tensor = torch.randint(
        86400,
        size=(batch_size, max_seq_len),
        device="cuda",
    )
    timestamps = timestamp_deltas.cumsum(dim=1)
    timestamps_triton = torch.cat([timestamps, timestamps[:, max_seq_len - 1 :]], dim=1)

    ts_weights: torch.Tensor = (
        torch.empty(
            (num_buckets + 1,),
            device="cuda",
            dtype=weights_dtype,
        )
        .uniform_(-0.1, 0.1)
        .requires_grad_()
    )

    pos_weights_size = 2 * max_seq_len - 1

    pos_weights: torch.Tensor = (
        torch.empty(
            (pos_weights_size,),
            device="cuda",
            dtype=weights_dtype,
        )
        .uniform_(-1.0, 1.0)
        .requires_grad_()
    )

    # torch implementation
    relative_bias = RelativeBucketedTimeAndPositionBasedBias(
        max_seq_len=max_seq_len,
        num_buckets=num_buckets,
        bucketization_fn=lambda x: (
            torch.log((x + time_delta).clamp(min=1e-6) / bucket_settings[1]) / bucket_settings[2]
        )
        .clamp(min=0)
        .long(),
    )
    relative_bias._ts_w = torch.nn.Parameter(ts_weights)
    relative_bias._pos_w = torch.nn.Parameter(pos_weights)
    attn_mask = torch.triu(
        torch.ones((max_seq_len, max_seq_len), dtype=torch.bool),
        diagonal=1,
    ).cuda()

    gamma = nn.Parameter(torch.randn((heads, hidden_dim), device="cuda", dtype=dtype))
    beta = nn.Parameter(torch.randn((heads, hidden_dim), device="cuda", dtype=dtype))

    return (
        q,
        k,
        v,
        u,
        attn_mask,
        relative_bias,
        timestamps,
        seq_offsets,
        max_seq_len,
        gamma,
        beta,
        timestamps_triton,
    )


def hstu_test_torch_forward_kernel1(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    attn_mask: torch.Tensor,
    rel_attn_bias: RelativeAttentionBiasModule,
    heads: int,
    attn_dim: int,
    hidden_dim: int,
    seq_offsets: torch.Tensor,
    is_causal: bool,
):

    L = int(seq_offsets[-1].item())
    qkv_out, _, _ = _hstu_attention_no_cache(
        num_heads=heads,
        attention_dim=attn_dim,
        linear_dim=hidden_dim,
        q=q.view(L, -1),
        k=k.view(L, -1),
        v=v.view(L, -1),
        x_offsets=seq_offsets,
        all_timestamps=None,  # first of all, we make the all_timestamps = None
        invalid_attn_mask=1.0 - attn_mask.to(torch.float32),  # Upper triangular matrix #no mask
        rel_attn_bias=None,  # first of all, we make the rel_attn_bias = None
        is_causal=is_causal,
    )

    return qkv_out


def hstu_test_torch_forward_kernel2(
    P: torch.Tensor,
    gamma: torch.Tensor,
    beta: torch.Tensor,
    U: torch.Tensor,
):
    # L = P.size(1)
    mean = mean.unsqueeze(1)
    variance = variance.unsqueeze(1)
    # variance.fill_(float(100))
    denominator = 1.0 / torch.sqrt(variance + 1e-05)
    # beta_clone = beta.clone()
    # beta_clone.fill_(float(1e-5))
    # P_1d = P.view(-1)
    # mean_1d = mean.view(-1)
    # gamma_1d = gamma.view(-1)

    # print("89 P_1d index is {:.9f}, mean_1d is {:.9f}, gamma_1d is {:.9f}".format(float(P_1d[89]), float(mean_1d[89 // L]), float(gamma_1d[89 % L])))
    # print("88 P_1d index is {:.9f}, mean_1d is {:.9f}, gamma_1d is {:.9f}".format(float(P_1d[88]), float(mean_1d[88 // L]), float(gamma_1d[88 % L])))
    # print("90 P_1d index is {:.9f}, mean_1d is {:.9f}, gamma_1d is {:.9f}".format(float(P_1d[90]), float(mean_1d[90 // L]), float(gamma_1d[90 % L])))
    print("variance is {}, beta is {}".format(variance, beta))
    R = (
        ((P.to(torch.float32)) - mean.to(torch.float32))
        * denominator.to(torch.float32)
        * gamma.to(torch.float32)
        + beta.to(torch.float32)
    ).to(torch.float16)
    # R_1d = R.view(-1)
    # U_1d = U.view(-1)
    O = R * U
    # O_1d = O.view(-1)
    # print()
    # print("R index is {:.9f}, U index is {:.9f}, O index is {:.9f}".format(float(R_1d[89]), float(U_1d[89]), float(O_1d[89])))
    # print("88 R index is {:.9f}, U index is {:.9f}, O index is {:.9f}".format(float(R_1d[88]), float(U_1d[88]), float(O_1d[88])))
    # print("90 R index is {:.9f}, U index is {:.9f}, O index is {:.9f}".format(float(R_1d[90]), float(U_1d[90]), float(O_1d[90])))
    return O


def hstu_test_torch_forward_kernel2_layernorm(
    P: torch.Tensor,
    gamma: torch.Tensor,
    beta: torch.Tensor,
    U: torch.Tensor,
):
    R = F.layer_norm(P, normalized_shape=[P.size(1)], weight=gamma, bias=beta, eps=1e-05)
    O = R * U
    return O


if __name__ == "__main__":
    q, k, v, u, attn_mask, relative_bias, timestamps, seq_offsets, max_seq_len = generate_input(
        batch_size=32,
        heads=8,
        max_uih_len=1024,
        max_targets=0,
        attn_dim=128,
        hidden_dim=256,
        num_buckets=100,
        bucket_settings=float,
        dtype=torch.float,
        weights_dtype=torch.float,
    )
    # kv_out, all_mean, all_variance, gamma, beta, u, mean_head, var_head
    P, all_mean, all_variance, gamma, beta, mean_head, var_head = hstu_test_torch_forward_kernel1(
        q,
        k,
        v,
        attn_mask,
        rel_attn_bias=None,
        heads=8,
        attn_dim=128,
        hidden_dim=256,
        seq_offsets=seq_offsets,
    )

    O, U_Caret, U_tilde = hstu_test_torch_forward_kernel2(P, all_mean, all_variance, gamma, beta, U)

