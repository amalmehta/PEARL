"""Aggregate runs/ into results/summary.json + results/RESULTS.md and draw figures/*.png.

Every number in the writeup and on the site comes from results/summary.json, which this
script regenerates from the raw run logs.
"""
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pearl.envs import make_env  # noqa: E402

ENV_LABEL = {"point": "Point-Robot (dense)", "sparse_point": "Sparse Point-Robot",
             "point_wind": "Point-Wind (invented)"}
VARIANT_LABEL = {"pearl": "PEARL", "deterministic": "Deterministic z", "rnn_transitions": "RNN, shuffled transitions",
                 "rnn_trajectories": "RNN, whole trajectories", "ctx_offpolicy": "Context from whole buffer",
                 "ctx_rlbatch": "Context = RL batch", "ctx_full": "PEARL, context batch 1024"}
# warm palette; ablation groups share a hue family
COLORS = {"pearl": "#c2410c", "deterministic": "#2563eb", "rnn_transitions": "#7c3aed",
          "rnn_trajectories": "#a78bfa", "ctx_offpolicy": "#0f766e", "ctx_rlbatch": "#5eead4",
          "ctx_full": "#b45309"}
ABLATIONS = {"Probabilistic vs deterministic z": ["pearl", "deterministic"],
             "Encoder architecture": ["pearl", "rnn_transitions", "rnn_trajectories"],
             "Where the context is sampled from": ["pearl", "ctx_offpolicy", "ctx_rlbatch"]}


def load():
    runs = {}
    for f in sorted((ROOT / "runs").glob("*/*/seed*/metrics.json")):
        m = json.loads(f.read_text())
        runs.setdefault((m["config"]["env"], m["config"]["variant"]), []).append(m)
    return runs


def curves(seed_runs):
    evals = [[r for r in m["metrics"] if "eval_final" in r] for m in seed_runs]
    n = min(len(e) for e in evals)
    steps = np.array([r["env_steps"] for r in evals[0][:n]])
    final = np.array([[r["eval_final"] for r in e[:n]] for e in evals])
    adapt = np.array([e[n - 1]["eval_curve"] for e in evals])
    zvar = np.array([e[n - 1]["eval_z_var"] for e in evals])
    return steps, final, adapt, zvar


def random_policy_return(env_name, n_traj=200, seed=0):
    """Control: uniformly random actions, the same reward the eval reports."""
    env, rng = make_env(env_name), np.random.default_rng(seed)
    rets = []
    for i in range(n_traj):
        env.reset_task(80 + i % 20)
        tot = 0.0
        for _ in range(env.horizon):
            _, r, _, info = env.step(rng.uniform(-1, 1, 2))
            tot += info.get("sparse_reward", r) if env.sparse else r
        rets.append(tot)
    return float(np.mean(rets))


def oracle_return(env_name, n_traj=200):
    """Upper reference: knows the task, moves straight at the goal at full speed (cancelling wind)."""
    env, rets = make_env(env_name), []
    for i in range(n_traj):
        env.reset_task(80 + i % 20); env.seed(i)
        s, tot = env.reset(), 0.0
        for _ in range(env.horizon):
            a = np.clip((env.goal - s - getattr(env, "wind", 0.0)) / 0.1, -1, 1)
            s, r, _, info = env.step(a)
            tot += info.get("sparse_reward", r) if env.sparse else r
        rets.append(tot)
    return float(np.mean(rets))


def band(ax, x, ys, color, label):
    for y in ys:
        ax.plot(x, y, color=color, alpha=0.18, lw=1)
    m, s = ys.mean(0), ys.std(0)
    ax.plot(x, m, color=color, lw=2, label=f"{label} (n={len(ys)})")
    ax.fill_between(x, m - s, m + s, color=color, alpha=0.15, lw=0)


def style(ax, title, xlabel, ylabel):
    ax.set_title(title, fontsize=11, loc="left")
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(alpha=0.25)


def main():
    runs = load()
    if not runs:
        print("no runs yet"); return
    plt.rcParams.update({"font.family": "sans-serif", "font.size": 9, "axes.facecolor": "#fffdf9",
                         "figure.facecolor": "#fffdf9"})
    figs = ROOT / "figures"; figs.mkdir(exist_ok=True)
    res = ROOT / "results"; res.mkdir(exist_ok=True)
    summary = {"runs": {}, "random_policy": {}, "oracle": {}}
    for (env, variant), seed_runs in runs.items():
        steps, final, adapt, zvar = curves(seed_runs)
        summary["runs"][f"{env}/{variant}"] = dict(
            env=env, variant=variant, seeds=[m["seed"] for m in seed_runs], env_steps=steps.tolist(),
            final_return=final.tolist(), adaptation=adapt.tolist(), z_var=zvar.tolist(),
            final_mean=float(final[:, -1].mean()), final_std=float(final[:, -1].std()),
            first_traj_mean=float(adapt[:, 0].mean()), minutes=[round(m["metrics"][-1]["seconds"] / 60, 1)
                                                               for m in seed_runs])
    for env in {e for e, _ in runs}:
        summary["random_policy"][env] = random_policy_return(env)
        summary["oracle"][env] = oracle_return(env)

    # Fig 1: PEARL learning curves on each family
    envs = [e for e in ENV_LABEL if (e, "pearl") in runs]
    fig, axes = plt.subplots(1, len(envs), figsize=(4.2 * len(envs), 3.2), squeeze=False)
    for ax, env in zip(axes[0], envs):
        steps, final, _, _ = curves(runs[(env, "pearl")])
        band(ax, steps / 1e3, final, COLORS["pearl"], "PEARL")
        ax.axhline(summary["random_policy"][env], color="#78716c", ls="--", lw=1, label="random actions")
        ax.axhline(summary["oracle"][env], color="#78716c", ls=":", lw=1, label="oracle (knows the task)")
        style(ax, ENV_LABEL[env], "env steps (thousands)", "return, last eval trajectory")
        ax.legend(frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(figs / "learning_curves.png", dpi=160); plt.close(fig)

    # Fig 2: adaptation within one meta-test episode
    fig, axes = plt.subplots(1, len(envs), figsize=(4.2 * len(envs), 3.2), squeeze=False)
    for ax, env in zip(axes[0], envs):
        _, _, adapt, _ = curves(runs[(env, "pearl")])
        x = np.arange(1, adapt.shape[1] + 1)
        band(ax, x, adapt, COLORS["pearl"], "PEARL")
        style(ax, ENV_LABEL[env], "trajectory in the meta-test episode", "return")
        ax.set_xticks(x)
    fig.tight_layout(); fig.savefig(figs / "adaptation.png", dpi=160); plt.close(fig)

    # Fig 3: ablations on dense Point-Robot
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.4))
    for ax, (title, variants) in zip(axes, ABLATIONS.items()):
        for v in variants:
            if ("point", v) in runs:
                steps, final, _, _ = curves(runs[("point", v)])
                band(ax, steps / 1e3, final, COLORS[v], VARIANT_LABEL[v])
        style(ax, title, "env steps (thousands)", "return")
        ax.legend(frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(figs / "ablations.png", dpi=160); plt.close(fig)

    (res / "summary.json").write_text(json.dumps(summary))
    lines = ["# Results", "", "Generated by `experiments/make_figures.py` from `runs/`. Mean ± std across seeds of",
             "the return of the LAST trajectory of a meta-test episode on the 20 held-out tasks.", "",
             "| Env | Variant | Seeds | First trajectory | Last trajectory | Random actions | Oracle | Minutes/run |",
             "|---|---|---|---|---|---|---|---|"]
    for k, r in sorted(summary["runs"].items()):
        lines.append(f"| {ENV_LABEL[r['env']]} | {VARIANT_LABEL[r['variant']]} | {len(r['seeds'])} | "
                     f"{r['first_traj_mean']:.2f} | {r['final_mean']:.2f} ± {r['final_std']:.2f} | "
                     f"{summary['random_policy'][r['env']]:.2f} | {summary['oracle'][r['env']]:.2f} | {np.mean(r['minutes']):.0f} |")
    (res / "RESULTS.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
