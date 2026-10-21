"""The two pieces of maths at the heart of PEARL's inference network.

q(z | c_1..N) is proportional to prod_n Psi(z | c_n), where each factor is a diagonal Gaussian.
The product of Gaussians is again Gaussian:
    1/sigma^2 = sum_n 1/sigma_n^2          (precisions add)
    mu        = sigma^2 * sum_n mu_n / sigma_n^2   (precision-weighted mean)
So each transition adds evidence and the posterior narrows as context grows.
"""
import torch


def product_of_gaussians(mus, sigmas_sq, dim=-2):
    """mus, sigmas_sq: (..., n, d) -> mu, sigma_sq: (..., d). Clamp as in oyster."""
    sigmas_sq = sigmas_sq.clamp(min=1e-7)
    sigma_sq = 1.0 / torch.sum(1.0 / sigmas_sq, dim=dim)
    mu = sigma_sq * torch.sum(mus / sigmas_sq, dim=dim)
    return mu, sigma_sq


def kl_to_standard_normal(mu, sigma_sq):
    """KL(N(mu, diag sigma_sq) || N(0, I)), summed over the last dim.

    = 0.5 * sum(sigma_sq + mu^2 - 1 - log sigma_sq)
    """
    return 0.5 * torch.sum(sigma_sq + mu.pow(2) - 1.0 - torch.log(sigma_sq), dim=-1)
