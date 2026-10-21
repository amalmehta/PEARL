"""PEARL meta-training: data collection, the SAC + encoder update, and meta-test evaluation.

Mirrors oyster's rl_algorithm.train / sac._take_step / collect_paths. Departures are marked
DEVIATION and listed in docs/SYSTEM-DESIGN.md.
"""
import json
import logging
import time
from pathlib import Path

import numpy as np
import torch
from torch import nn

from .agent import PEARLAgent
from .buffers import MultiTaskBuffer
from .envs import make_env
from .networks import MLP

log = logging.getLogger("pearl")


class PEARL:
    def __init__(self, cfg, seed=0, out_dir=None):
        self.cfg, self.seed = cfg, seed
        self.rng = np.random.default_rng(seed)
        torch.manual_seed(seed)
        self.env = make_env(cfg["env"], cfg["n_tasks"])
        self.env.seed(seed)
        self.train_tasks = list(range(cfg["n_train_tasks"]))
        self.eval_tasks = list(range(cfg["n_tasks"] - cfg["n_eval_tasks"], cfg["n_tasks"]))
        self.use_next_obs = self.env.use_next_obs_in_context
        o, a = self.env.obs_dim, self.env.action_dim
        self.context_dim = o + a + 1 + (o if self.use_next_obs else 0)

        self.agent = PEARLAgent(o, a, self.context_dim, cfg)
        d, h = cfg["latent_size"], cfg["net_size"]
        self.qf1, self.qf2 = MLP(o + a + d, [h] * 3, 1), MLP(o + a + d, [h] * 3, 1)
        self.vf, self.target_vf = MLP(o + d, [h] * 3, 1), MLP(o + d, [h] * 3, 1)
        self.target_vf.load_state_dict(self.vf.state_dict())

        adam = torch.optim.Adam
        self.policy_opt = adam(self.agent.policy.parameters(), lr=cfg["policy_lr"])
        self.qf1_opt = adam(self.qf1.parameters(), lr=cfg["qf_lr"])
        self.qf2_opt = adam(self.qf2.parameters(), lr=cfg["qf_lr"])
        self.vf_opt = adam(self.vf.parameters(), lr=cfg["vf_lr"])
        self.context_opt = adam(self.agent.encoder.parameters(), lr=cfg["context_lr"])

        cap = 100_000
        self.replay = MultiTaskBuffer(cfg["n_tasks"], o, a, cap)      # everything: feeds the RL batch
        self.enc_replay = MultiTaskBuffer(cfg["n_tasks"], o, a, cap)  # recent data: feeds the context
        self.env_steps = 0
        self.out_dir = Path(out_dir) if out_dir else None

    # ---- data -----------------------------------------------------------------------
    def _context_features(self, b):
        r = b["sparse_rewards"] if self.env.sparse else b["rewards"]  # encoder sees sparse rewards
        parts = [b["obs"], b["actions"], r] + ([b["next_obs"]] if self.use_next_obs else [])
        return np.concatenate(parts, axis=-1)

    def sample_context(self, indices):
        cfg, n = self.cfg, self.cfg["embedding_batch_size"]
        out = []
        for i in indices:
            buf = self.replay[i] if cfg["context_sampling"] == "offpolicy" else self.enc_replay[i]
            b = buf.random_sequence(n, self.rng) if cfg["sequence_context"] else buf.random_batch(n, self.rng)
            out.append(self._context_features(b))
        return torch.as_tensor(np.stack(out))

    def sample_sac(self, indices):
        # oyster: "rewards are always dense" for the RL batch, even on sparse tasks
        batches = [self.replay[i].random_batch(self.cfg["batch_size"], self.rng) for i in indices]
        stacked = {k: torch.as_tensor(np.stack([b[k] for b in batches])) for k in batches[0]}
        return stacked, batches

    def rollout(self, z, deterministic=False, accum=None):
        env, H = self.env, self.cfg["max_path_length"]
        obs = env.reset()
        path = {k: [] for k in ("obs", "actions", "rewards", "sparse_rewards", "next_obs", "terminals")}
        for _ in range(H):
            a = self.agent.act(obs, z, deterministic)
            nxt, r, done, info = env.step(a)
            sr = info.get("sparse_reward", r)
            for k, v in zip(path, (obs, a, r, sr, nxt, float(done))):
                path[k].append(v)
            if accum is not None:
                feat = [obs, a, [sr if env.sparse else r]] + ([nxt] if self.use_next_obs else [])
                accum.append(np.concatenate(feat).astype(np.float32))
            obs = nxt
            if done:
                break
        return {k: np.asarray(v, dtype=np.float32).reshape(len(v), -1) for k, v in path.items()}

    def collect_data(self, task, num_samples, update_posterior_rate, add_to_enc=True):
        """Collect >= num_samples transitions. z ~ prior at first; if update_posterior_rate is
        finite, refit q(z|c) from the task's encoder buffer every that many trajectories."""
        self.env.reset_task(task)
        mu, var = self.agent.prior()
        n, trajs = 0, 0
        while n < num_samples:
            z = self.agent.sample_z(mu, var)  # resample every trajectory (oyster resample=1)
            path = self.rollout(z)
            self.replay[task].add_path(path)
            if add_to_enc:
                self.enc_replay[task].add_path(path)
            n += len(path["obs"])
            trajs += 1
            if update_posterior_rate != np.inf and trajs % update_posterior_rate == 0:
                with torch.no_grad():
                    mu, var = self.agent.infer(self.sample_context([task]))
        self.env_steps += n

    # ---- one meta-gradient step -----------------------------------------------------------
    def train_step(self, indices):
        cfg, T, B = self.cfg, len(indices), self.cfg["batch_size"]
        batch, raw = self.sample_sac(indices)
        if cfg["context_sampling"] == "rlbatch":
            context = torch.as_tensor(np.stack([self._context_features(b) for b in raw]))
        else:
            context = self.sample_context(indices)

        mu, var = self.agent.infer(context)
        task_z = self.agent.sample_z(mu, var)                     # (T, d), carries encoder grads
        flat = lambda x: x.reshape(T * B, -1)
        obs, act, nxt = flat(batch["obs"]), flat(batch["actions"]), flat(batch["next_obs"])
        rew, term = flat(batch["rewards"]) * cfg["reward_scale"], flat(batch["terminals"])
        z = task_z.repeat_interleave(B, dim=0)

        new_act, p_mean, p_log_std, log_pi = self.agent.policy(torch.cat([obs, z.detach()], -1))
        q1, q2 = self.qf1(obs, act, z), self.qf2(obs, act, z)    # encoder learns ONLY from the critic
        v_pred = self.vf(obs, z.detach())
        with torch.no_grad():
            target_v = self.target_vf(nxt, z)

        self.context_opt.zero_grad()
        kl = torch.tensor(0.0)
        if self.agent.use_ib:
            kl = self.agent.kl(mu, var)
            (cfg["kl_lambda"] * kl).backward(retain_graph=True)

        self.qf1_opt.zero_grad(); self.qf2_opt.zero_grad()
        q_target = rew + (1.0 - term) * cfg["discount"] * target_v
        qf_loss = ((q1 - q_target) ** 2).mean() + ((q2 - q_target) ** 2).mean()
        qf_loss.backward()
        self.qf1_opt.step(); self.qf2_opt.step(); self.context_opt.step()

        min_q_new = torch.min(self.qf1(obs, new_act, z.detach()), self.qf2(obs, new_act, z.detach()))
        vf_loss = ((v_pred - (min_q_new - log_pi).detach()) ** 2).mean()
        self.vf_opt.zero_grad(); vf_loss.backward(); self.vf_opt.step()
        with torch.no_grad():
            tau = cfg["soft_target_tau"]
            for t, s in zip(self.target_vf.parameters(), self.vf.parameters()):
                t.mul_(1 - tau).add_(tau * s)

        policy_loss = (log_pi - min_q_new).mean() \
            + cfg["policy_mean_reg_weight"] * p_mean.pow(2).mean() \
            + cfg["policy_std_reg_weight"] * p_log_std.pow(2).mean()
        self.policy_opt.zero_grad(); policy_loss.backward(); self.policy_opt.step()

        return dict(qf_loss=qf_loss.item(), vf_loss=vf_loss.item(), policy_loss=policy_loss.item(),
                    kl=kl.item(), z_var=var.mean().item())

    # ---- meta-test ------------------------------------------------------------------
    @torch.no_grad()
    def evaluate(self, tasks=None, keep_paths=False):
        """Online adaptation: explore with z ~ prior, then refit q(z|c) on the accumulated context
        after each trajectory once num_exp_traj_eval have been collected (oyster collect_paths)."""
        cfg = self.cfg
        tasks = self.eval_tasks if tasks is None else tasks
        n_traj = int(np.ceil(cfg["num_steps_per_eval"] / cfg["max_path_length"]))
        returns, variances, kept = [], [], []
        for t in tasks:
            self.env.reset_task(t)
            mu, var = self.agent.prior()
            z = self.agent.sample_z(mu, var)
            ctx, rets, vs, paths = [], [], [], []
            for k in range(n_traj):
                p = self.rollout(z, deterministic=True, accum=ctx)
                rets.append(float((p["sparse_rewards"] if self.env.sparse else p["rewards"]).sum()))
                vs.append(float(var.mean()))
                if keep_paths:
                    paths.append(p["next_obs"].tolist())
                if k + 1 >= cfg["num_exp_traj_eval"]:
                    mu, var = self.agent.infer(torch.as_tensor(np.stack(ctx))[None])
                z = self.agent.sample_z(mu, var)
            returns.append(rets)
            variances.append(vs)
            if keep_paths:
                kept.append(dict(task=t, goal=np.asarray(self.env.tasks[t]).tolist(), paths=paths))
        out = dict(returns=np.asarray(returns), z_var=np.asarray(variances))
        if keep_paths:
            out["paths"] = kept
        return out

    # ---- the loop -------------------------------------------------------------------
    def train(self, eval_every=5):
        cfg = self.cfg
        t0 = time.time()
        metrics = []
        for task in self.train_tasks:
            self.collect_data(task, cfg["num_initial_steps"], np.inf)
        for it in range(cfg["num_iterations"]):
            for _ in range(cfg["num_tasks_sample"]):
                task = int(self.rng.integers(len(self.train_tasks)))
                self.enc_replay[task].clear()  # the encoder only ever sees recent data
                if cfg["num_steps_prior"] > 0:
                    self.collect_data(task, cfg["num_steps_prior"], np.inf)
                if cfg["num_steps_posterior"] > 0:
                    self.collect_data(task, cfg["num_steps_posterior"], cfg["update_post_train"])
                if cfg["num_extra_rl_steps_posterior"] > 0:
                    self.collect_data(task, cfg["num_extra_rl_steps_posterior"], cfg["update_post_train"],
                                      add_to_enc=False)
            stats = []
            for _ in range(cfg["num_train_steps_per_itr"]):
                idx = self.rng.choice(self.train_tasks, cfg["meta_batch"])
                stats.append(self.train_step(idx))
            row = dict(itr=it, env_steps=self.env_steps, seconds=round(time.time() - t0, 1),
                       **{k: float(np.mean([s[k] for s in stats])) for k in stats[0]})
            if (it + 1) % eval_every == 0 or it == cfg["num_iterations"] - 1:
                ev = self.evaluate()
                curve = ev["returns"].mean(0)
                row.update(eval_curve=curve.tolist(), eval_final=float(curve[-1]),
                           eval_first=float(curve[0]), eval_z_var=ev["z_var"].mean(0).tolist())
                log.info("%s/%s seed %d itr %d  first %.2f  final %.2f  kl %.2f  %.0fs", cfg["env"],
                         cfg["variant"], self.seed, it, row["eval_first"], row["eval_final"], row["kl"],
                         row["seconds"])
            metrics.append(row)
            if self.out_dir:
                self._save(metrics)
        return metrics

    def _save(self, metrics):
        self.out_dir.mkdir(parents=True, exist_ok=True)
        (self.out_dir / "metrics.json").write_text(json.dumps(dict(config=self.cfg, seed=self.seed,
                                                                  metrics=metrics)))
        torch.save(dict(agent=self.agent.state_dict(), cfg=self.cfg), self.out_dir / "agent.pt")
