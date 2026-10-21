import numpy as np
import pytest
import torch

from pearl.buffers import TaskBuffer
from pearl.config import VARIANTS, make_config
from pearl.envs import PointRobot, PointWind, SparsePointRobot
from pearl.gaussian import kl_to_standard_normal, product_of_gaussians
from pearl.trainer import PEARL


# ---- maths ----------------------------------------------------------------------------
def test_product_of_gaussians_matches_closed_form():
    # N(0, 1) * N(2, 1) = N(1, 0.5)
    mu, var = product_of_gaussians(torch.tensor([[0.0], [2.0]]), torch.tensor([[1.0], [1.0]]))
    assert torch.allclose(mu, torch.tensor([1.0])) and torch.allclose(var, torch.tensor([0.5]))


def test_product_of_gaussians_is_permutation_invariant_and_narrows():
    g = torch.Generator().manual_seed(0)
    mus, var = torch.randn(7, 5, generator=g), torch.rand(7, 5, generator=g) + 0.1
    a = product_of_gaussians(mus, var)
    perm = torch.randperm(7, generator=g)
    c = product_of_gaussians(mus[perm], var[perm])
    assert torch.allclose(a[0], c[0], atol=1e-6) and torch.allclose(a[1], c[1], atol=1e-6)
    assert torch.all(a[1] <= var.min(0).values + 1e-7)  # more evidence never widens the posterior


def test_product_matches_numeric_density_product():
    # check against brute-force multiplication of densities on a grid
    x = torch.linspace(-6, 6, 20001)
    m, s2 = torch.tensor([0.3, -1.2, 2.0]), torch.tensor([0.5, 2.0, 1.5])
    logp = (-(x[:, None] - m) ** 2 / (2 * s2)).sum(1)
    p = torch.exp(logp - logp.max()); p = p / p.sum()
    mean = (p * x).sum(); var = (p * (x - mean) ** 2).sum()
    mu, v = product_of_gaussians(m[:, None], s2[:, None])
    assert abs(mean - mu.item()) < 1e-3 and abs(var - v.item()) < 1e-3


def test_kl_matches_torch_distributions():
    mu, var = torch.randn(4, 5), torch.rand(4, 5) + 0.05
    ref = torch.distributions.kl_divergence(torch.distributions.Normal(mu, var.sqrt()),
                                            torch.distributions.Normal(0.0, 1.0)).sum(-1)
    assert torch.allclose(kl_to_standard_normal(mu, var), ref, atol=1e-5)
    assert torch.allclose(kl_to_standard_normal(torch.zeros(5), torch.ones(5)), torch.tensor(0.0))


# ---- environments (checked against oyster's point_robot.py) ----------------------------------
def test_point_tasks_match_oyster_seed_stream():
    np.random.seed(1337)
    expected = [[np.random.uniform(-1.0, 1.0), np.random.uniform(-1.0, 1.0)] for _ in range(100)]
    assert np.allclose(np.stack(PointRobot().tasks), expected)


def test_sparse_tasks_and_reward():
    env = SparsePointRobot()
    goals = np.stack(env.tasks)
    assert np.allclose(np.linalg.norm(goals, axis=1), 1.0) and goals[:, 1].min() >= -1e-9
    assert env.sparsify(-0.5) == 0.0 and env.sparsify(-0.1) == pytest.approx(0.9)
    env.reset_task(0)
    assert np.allclose(env.reset(), 0.0)  # sparse env always starts at the origin


def test_actions_are_rescaled_and_clipped():
    env = PointRobot(); env.reset_task(0); s = env.state.copy()
    obs, *_ = env.step(np.array([5.0, -5.0]))
    assert np.allclose(obs - s, [0.1, -0.1])


def test_wind_moves_the_agent():
    env = PointWind(); env.reset_task(3); s = env.state.copy()
    obs, *_ = env.step(np.zeros(2))
    assert np.allclose(obs - s, env.tasks[3]) and np.all(np.abs(np.stack(env.tasks)) <= 0.08)


# ---- buffers --------------------------------------------------------------------------
def _path(n, start):
    v = np.arange(start, start + n, dtype=np.float32)[:, None]
    two = np.repeat(v, 2, 1)
    return dict(obs=two, actions=two, rewards=v, sparse_rewards=v, next_obs=two, terminals=v * 0)


def test_sequence_sampling_keeps_trajectories_in_order():
    buf, rng = TaskBuffer(2, 2, 1000), np.random.default_rng(0)
    for k in range(5):
        buf.add_path(_path(20, 100 * k))
    seq = buf.random_sequence(40, rng)["rewards"][:, 0]
    assert np.all(np.diff(seq[:20]) == 1) and seq[0] % 100 == 0


def test_ring_buffer_wraps():
    buf = TaskBuffer(2, 2, 50)
    for k in range(6):
        buf.add_path(_path(20, 100 * k))
    assert buf.size == 50 and all(s < 50 for s in buf.episode_starts)


# ---- the algorithm --------------------------------------------------------------------
TINY = dict(n_tasks=6, n_train_tasks=4, n_eval_tasks=2, net_size=16, encoder_hidden=(16, 16, 16),
            batch_size=8, meta_batch=3, embedding_batch_size=8, embedding_mini_batch_size=8,
            num_initial_steps=20, num_tasks_sample=1, num_steps_prior=20, num_steps_posterior=20,
            num_extra_rl_steps_posterior=20, num_train_steps_per_itr=2, num_iterations=2,
            num_steps_per_eval=40, num_exp_traj_eval=1)


@pytest.mark.parametrize("env", ["point", "sparse_point", "point_wind"])
@pytest.mark.parametrize("variant", list(VARIANTS))
def test_every_env_and_variant_trains(env, variant):
    alg = PEARL(make_config(env, variant, **TINY), seed=0)
    metrics = alg.train(eval_every=1)
    assert len(metrics) == 2 and np.isfinite(metrics[-1]["qf_loss"])
    assert len(metrics[-1]["eval_curve"]) == 2


def test_encoder_gets_gradient_from_critic_not_policy():
    alg = PEARL(make_config("point", **TINY), seed=0)
    for t in alg.train_tasks:
        alg.collect_data(t, 20, np.inf)
    ctx = alg.sample_context([0, 1])
    mu, var = alg.agent.infer(ctx)
    z = alg.agent.sample_z(mu, var)
    obs = torch.zeros(2, 2)
    # policy path uses z.detach(): no gradient may reach the encoder
    alg.agent.policy(torch.cat([obs, z.detach()], -1))[3].sum().backward(retain_graph=True)
    assert all(p.grad is None for p in alg.agent.encoder.parameters())
    alg.qf1(obs, torch.zeros(2, 2), z).sum().backward()
    assert any(p.grad is not None and p.grad.abs().sum() > 0 for p in alg.agent.encoder.parameters())


def test_posterior_narrows_with_more_context():
    alg = PEARL(make_config("point", **TINY), seed=0)
    alg.collect_data(0, 200, np.inf)
    small = alg.agent.infer(torch.as_tensor(alg._context_features(alg.enc_replay[0].random_batch(4, alg.rng)))[None])[1]
    big = alg.agent.infer(torch.as_tensor(alg._context_features(alg.enc_replay[0].random_batch(64, alg.rng)))[None])[1]
    assert big.mean() < small.mean()


def test_seeded_runs_are_reproducible():
    a = PEARL(make_config("point", **TINY), seed=3).train()
    b = PEARL(make_config("point", **TINY), seed=3).train()
    assert a[-1]["qf_loss"] == b[-1]["qf_loss"]
