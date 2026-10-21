"""Hyperparameters.

PAPER: copied from oyster configs/default.py + configs/<env>.json (commit on master,
fetched 2026-10-20). BUDGET: laptop-budget overrides, applied on top and listed in
docs/SYSTEM-DESIGN.md. They change how long we train, never what the algorithm does.
"""
from copy import deepcopy

PAPER_DEFAULT = dict(
    latent_size=5, net_size=300, encoder_hidden=(200, 200, 200),
    n_train_tasks=80, n_eval_tasks=20, n_tasks=100,
    meta_batch=16, num_iterations=500, num_initial_steps=2000, num_tasks_sample=5,
    num_steps_prior=400, num_steps_posterior=0, num_extra_rl_steps_posterior=400,
    num_train_steps_per_itr=2000, num_steps_per_eval=600, batch_size=256,
    embedding_batch_size=64, embedding_mini_batch_size=64, max_path_length=200,
    discount=0.99, soft_target_tau=0.005, policy_lr=3e-4, qf_lr=3e-4, vf_lr=3e-4,
    context_lr=3e-4, reward_scale=5.0, kl_lambda=0.1, use_information_bottleneck=True,
    recurrent=False, update_post_train=1, num_exp_traj_eval=1,
    policy_mean_reg_weight=1e-3, policy_std_reg_weight=1e-3,
    # not oyster flags: our names for the paper's ablation switches
    context_sampling="recent",   # recent | offpolicy | rlbatch   (paper Fig. 5c)
    sequence_context=False,      # RNN on whole trajectories vs shuffled transitions (Fig. 5b)
)

PAPER_ENV = {
    # configs/point-robot.json
    "point": dict(num_initial_steps=200, num_steps_prior=200, num_steps_posterior=0,
                  num_extra_rl_steps_posterior=200, num_train_steps_per_itr=1000,
                  num_steps_per_eval=60, max_path_length=20, reward_scale=100.0, kl_lambda=0.1),
    # configs/sparse-point-robot.json
    "sparse_point": dict(num_initial_steps=200, num_tasks_sample=10, num_steps_prior=100,
                         num_steps_posterior=900, num_extra_rl_steps_posterior=0,
                         num_train_steps_per_itr=1000, num_steps_per_eval=400,
                         embedding_batch_size=1024, embedding_mini_batch_size=1024,
                         max_path_length=20, discount=0.90, reward_scale=100.0,
                         kl_lambda=1.0, num_exp_traj_eval=5),
    # INVENTED env, so no paper config: reuse the dense point-robot settings
    "point_wind": dict(num_initial_steps=200, num_steps_prior=200, num_steps_posterior=0,
                       num_extra_rl_steps_posterior=200, num_train_steps_per_itr=1000,
                       num_steps_per_eval=60, max_path_length=20, reward_scale=100.0,
                       kl_lambda=0.1),
}

# Laptop budget (see docs/SYSTEM-DESIGN.md, "Run budget").
BUDGET = {
    # all three: 8 tasks x 128 transitions per step instead of 16 x 256, 128-unit nets instead of 300,
    # 250 gradient steps per iteration instead of 1000, 150 iterations instead of 500
    env: dict(num_iterations=150, num_train_steps_per_itr=250, net_size=128, meta_batch=8, batch_size=128,
              **({"embedding_batch_size": 256, "embedding_mini_batch_size": 256} if env == "sparse_point" else {}))
    for env in ("point", "sparse_point", "point_wind")
}

VARIANTS = {
    "pearl": {},
    "deterministic": dict(use_information_bottleneck=False),
    "rnn_transitions": dict(recurrent=True, sequence_context=False),
    "rnn_trajectories": dict(recurrent=True, sequence_context=True),
    "ctx_offpolicy": dict(context_sampling="offpolicy"),
    "ctx_rlbatch": dict(context_sampling="rlbatch"),
}


def make_config(env, variant="pearl", budget=True, **overrides):
    cfg = deepcopy(PAPER_DEFAULT)
    cfg.update(PAPER_ENV[env])
    if budget:
        cfg.update(BUDGET[env])
    cfg.update(VARIANTS[variant])
    cfg.update(overrides)
    cfg["env"], cfg["variant"] = env, variant
    return cfg
