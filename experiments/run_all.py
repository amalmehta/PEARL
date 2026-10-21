"""Run the whole experiment suite, then aggregate and plot.

    python experiments/run_all.py              # everything (skips finished runs)
    python experiments/run_all.py --only point/pearl --seeds 0
    python experiments/run_all.py --plots-only

Runs go to runs/<env>/<variant>/seed<k>/ (git-ignored). Aggregates go to results/.
"""
import argparse
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pearl.config import make_config  # noqa: E402

SEEDS = [0, 1, 2]
SUITE = [
    # main result: PEARL on every task family
    ("point", "pearl"), ("sparse_point", "pearl"), ("point_wind", "pearl"),
    # paper Sec. 6.3 ablations, on dense Point-Robot
    ("point", "deterministic"),
    ("point", "rnn_transitions"), ("point", "rnn_trajectories"),
    ("point", "ctx_offpolicy"), ("point", "ctx_rlbatch"),
]


def run_dir(env, variant, seed):
    return ROOT / "runs" / env / variant / f"seed{seed}"


def is_done(env, variant, seed):
    f = run_dir(env, variant, seed) / "metrics.json"
    if not f.exists():
        return False
    m = json.loads(f.read_text())
    return len(m["metrics"]) >= make_config(env, variant)["num_iterations"]


def launch(job, threads):
    env, variant, seed = job
    out = run_dir(env, variant, seed)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    with open(out / "train.log", "w") as logf:
        code = subprocess.call([sys.executable, "-m", "pearl.train", "--env", env, "--variant", variant,
                                "--seed", str(seed), "--threads", str(threads), "--out", str(out)],
                               cwd=ROOT, stdout=logf, stderr=subprocess.STDOUT)
    print(f"{'ok ' if code == 0 else 'FAIL'} {env}/{variant}/seed{seed} in {time.time() - t0:.0f}s", flush=True)
    return code


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--threads", type=int, default=2)
    p.add_argument("--seeds", type=int, nargs="*", default=SEEDS)
    p.add_argument("--only", nargs="*", default=None, help="env/variant pairs to run")
    p.add_argument("--plots-only", action="store_true")
    a = p.parse_args()

    if not a.plots_only:
        suite = [tuple(s.split("/")) for s in a.only] if a.only else SUITE
        # longest runs first so the pool drains evenly
        jobs = [(e, v, s) for (e, v) in suite for s in a.seeds if not is_done(e, v, s)]
        jobs.sort(key=lambda j: (j[1].startswith("rnn"), j[0] == "sparse_point"), reverse=True)
        print(f"{len(jobs)} runs to do, {a.workers} at a time", flush=True)
        with ThreadPoolExecutor(a.workers) as pool:
            codes = list(pool.map(lambda j: launch(j, a.threads), jobs))
        if any(codes):
            print("some runs failed; see runs/**/train.log")
    subprocess.check_call([sys.executable, str(ROOT / "experiments" / "make_figures.py")], cwd=ROOT)


if __name__ == "__main__":
    main()
