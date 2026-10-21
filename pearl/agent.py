"""The PEARL agent: an inference network q(z|c) plus a policy pi(a|s,z)."""
import numpy as np
import torch

from .gaussian import kl_to_standard_normal, product_of_gaussians
from .networks import MlpEncoder, RecurrentEncoder, TanhGaussianPolicy


class PEARLAgent(torch.nn.Module):
    def __init__(self, obs_dim, action_dim, context_dim, cfg):
        super().__init__()
        self.latent_dim = d = cfg["latent_size"]
        self.use_ib = cfg["use_information_bottleneck"]
        enc_cls = RecurrentEncoder if cfg["recurrent"] else MlpEncoder
        # probabilistic: each factor outputs (mu, raw variance); deterministic: just z
        self.encoder = enc_cls(context_dim, list(cfg["encoder_hidden"]), 2 * d if self.use_ib else d)
        h = cfg["net_size"]
        self.policy = TanhGaussianPolicy(obs_dim + d, [h, h, h], action_dim)

    # ---- inference ------------------------------------------------------------------
    def prior(self, n_tasks=1):
        mu = torch.zeros(n_tasks, self.latent_dim)
        var = torch.ones_like(mu) if self.use_ib else torch.zeros_like(mu)
        return mu, var

    def infer(self, context):
        """context (tasks, n, feat) -> posterior mean and variance, each (tasks, latent)."""
        params = self.encoder(context)
        if self.use_ib:
            mu = params[..., : self.latent_dim]
            var = torch.nn.functional.softplus(params[..., self.latent_dim:])
            return product_of_gaussians(mu, var)
        # deterministic ablation: average the per-transition embeddings
        mu = params.mean(dim=1)
        return mu, torch.zeros_like(mu)

    def sample_z(self, mu, var):
        if not self.use_ib:
            return mu
        return mu + var.sqrt() * torch.randn_like(mu)  # reparameterised, so gradients reach the encoder

    def kl(self, mu, var):
        return kl_to_standard_normal(mu, var).sum()

    # ---- acting ---------------------------------------------------------------------
    @torch.no_grad()
    def act(self, obs, z, deterministic=False):
        x = torch.cat([torch.as_tensor(obs, dtype=torch.float32)[None], z], dim=-1)
        return self.policy(x, deterministic=deterministic)[0][0].numpy().astype(np.float64)
