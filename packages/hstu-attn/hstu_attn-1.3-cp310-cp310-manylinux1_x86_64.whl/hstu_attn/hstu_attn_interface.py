# Copyright (c) 2023, Tri Dao.
import torch
# so_dir='/home/scratch.binc_gpu_1/pure_hstu/hstu/'
# torch.classes.load_library(so_dir + 'hstu_attn_2_cuda.cpython-310-x86_64-linux-gnu.so')
import hstu_attn_2_cuda as hstu_attn_cuda



class HstuAttnVarlenFunc(torch.autograd.Function):
    @staticmethod
    def forward(
        ctx,
        q,  # need grad
        k,  # need grad
        v,  # need grad
        u,  # need grad
        seq_offsets,
        max_seqlen,
        RaB,  # don't need grad
        heads,
        attn_dim,
        hidden_dim, # attn_dim must equal to hidden_dim, and it must be a multiple of 8
        causal=False,
        gamma=None,
        beta=None,
    ):
        print("======= hello welcome to python ======")
        assert q.dim() == 3, "q shape should be (L, num_heads, head_dim)"
        assert k.dim() == 3, "k shape should be (L, num_heads, head_dim)"
        assert v.dim() == 3, "v shape should be (L, num_heads, head_dim)"
        assert u.dim() == 3, "u shape should be (L, num_heads, head_dim)"

        with torch.cuda.nvtx.range("hstu_varlen_fwd_kernel1"):
            P, mean_head, var_head = hstu_attn_cuda.hstu_varlen_fwd(
                q.reshape(-1, heads, attn_dim),
                k.reshape(-1, heads, attn_dim),
                v.reshape(-1, heads, hidden_dim),
                seq_offsets,
                seq_offsets,
                None,
                max_seqlen,
                max_seqlen,
                causal,
            )
        P = P[:, :, :hidden_dim].reshape(-1, heads * hidden_dim)

        layernorm_participate_training = True
        if gamma == None or beta == None:
            layernorm_participate_training = False
            gamma = torch.empty((heads, hidden_dim), dtype=q.dtype)
            beta = torch.empty((heads, hidden_dim), dtype=q.dtype)

        with torch.cuda.nvtx.range("hstu_varlen_fwd_kernel2"):
            O_cuda, All_mean, All_variance = hstu_attn_cuda.hstu_varlen_kernel2_fwd(
                P,
                u,
                mean_head,
                var_head,
                gamma,
                beta,
                heads,
                hidden_dim,
                layernorm_participate_training,
            )  # forward kernel2

        ctx.save_for_backward(
            q,
            k,
            v,
            u,
            O_cuda,
            seq_offsets,
            P,
            mean_head,
            var_head,
            gamma,
            beta,
            All_mean,
            All_variance,
        )
        ctx.max_seqlen = max_seqlen
        ctx.heads = heads
        ctx.attn_dim = attn_dim
        ctx.hidden_dim = hidden_dim
        ctx.Dlinear = hidden_dim
        ctx.layernorm_participate_training = layernorm_participate_training
        ctx.causal = causal
        return O_cuda.view(-1, heads, hidden_dim)

    @staticmethod
    def backward(ctx, dout, *args):
        (
            q,
            k,
            v,
            u,
            O_cuda,
            seq_offsets,
            P,
            mean_head,
            var_head,
            gamma,
            beta,
            All_mean,
            All_variance,
        ) = ctx.saved_tensors

        heads, Dlinear, layernorm_participate_training = (
            ctx.heads,
            ctx.Dlinear,
            ctx.layernorm_participate_training,
        )
        max_seqlen = ctx.max_seqlen
        attn_dim = ctx.attn_dim
        hidden_dim = ctx.hidden_dim
        with torch.cuda.nvtx.range("hstu_varlen_bwd_kernel2"):
            dU, dR, dGamma, dBeta, O1, O2 = hstu_attn_cuda.hstu_varlen_kernel2_bwd(
                P,
                u,
                dout,
                mean_head,
                var_head,
                gamma,
                beta, #if layernorm_participate_training == False, then the gamma and beta was not used, and the dGamma & dBeta is at::empty({0}, at::CUDA(dtype));
                heads,
                Dlinear,
                layernorm_participate_training,
            )

        if layernorm_participate_training == False:
            all_dGamma = None
            all_dBeta = None
        else:
            dGamma = dGamma.type(torch.float32) #as dGamma and dBeta need accumulation, so convert to float type
            dBeta = dBeta.type(torch.float32)
            all_dGamma = torch.sum(dGamma, dim=0).to(P.dtype)
            all_dBeta = torch.sum(dBeta, dim=0).to(P.dtype)

        with torch.cuda.nvtx.range("hstu_varlen_bwd_kernel1"):
            dq, dk, dv = hstu_attn_cuda.hstu_varlen_bwd(
                dR.view(-1, heads, hidden_dim),
                q.view(-1, heads, attn_dim),
                k.view(-1, heads, attn_dim),
                v.view(-1, heads, hidden_dim),
                O1.view(-1),
                O2.view(-1),
                gamma.view(heads, attn_dim),
                beta.view(heads, attn_dim),
                All_mean.view(-1),
                All_variance.view(-1),
                O_cuda.view(-1, heads, hidden_dim),
                None,
                None,
                None,
                seq_offsets,
                seq_offsets,
                max_seqlen,
                max_seqlen,
                ctx.causal,
                False,
            )
        # q & k grad shape
        return (
            dq.reshape(-1, heads, attn_dim),  # dq
            dk.reshape(-1, heads, attn_dim),  # dk
            dv.reshape(-1, heads, hidden_dim),  # dv
            dU.reshape(-1, heads, hidden_dim),  # dv
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            all_dGamma.reshape(heads, hidden_dim) if all_dGamma is not None else None, #TODO if gamma is None
            all_dBeta.reshape(heads, hidden_dim) if all_dBeta is not None else None,
        )


def hstu_attn_varlen_func(
    q,
    k,
    v,
    u,
    seq_offsets,
    max_seqlen,
    rab,
    heads,
    attn_dim,
    hidden_dim,
    causal=False,
    gamma=None,  # if layernorm The gamma and beta of layernorm do not participate in model training, gamma = beta = None
    beta=None,
):
    """ """
    assert attn_dim == hidden_dim, "Only support attn_dim == hidden_dim now."
    assert attn_dim % 8 == 0, "Only support attn_dim(hidden_dim) is a multiple of 8."
    return HstuAttnVarlenFunc.apply(
        q,
        k,
        v,
        u,
        seq_offsets,
        max_seqlen,
        rab,
        heads,
        attn_dim,
        hidden_dim,
        causal,
        gamma,
        beta,
    )


if __name__ == "__main__":
    print("main")

