"""Export a trained agent for the in-browser demo: weights as base64 float32, plus sample paths.

    python -m pearl.export runs/sparse_point/pearl/seed0 site/data/sparse_point.json
"""
import base64
import json
import sys
from pathlib import Path

import numpy as np
import torch

from .trainer import PEARL


def _b64(t):
    return base64.b64encode(t.detach().float().numpy().astype("<f4").tobytes()).decode()


def _mlp_layers(linears):
    return [dict(w=_b64(l.weight), b=_b64(l.bias), shape=list(l.weight.shape)) for l in linears]


def export(run_dir, out_file, n_paths=4):
    ckpt = torch.load(Path(run_dir) / "agent.pt")
    cfg = ckpt["cfg"]
    alg = PEARL(cfg, seed=123)
    alg.agent.load_state_dict(ckpt["agent"])
    pol, enc = alg.agent.policy, alg.agent.encoder
    if enc.recurrent:
        raise ValueError("the demo only runs the permutation-invariant encoder")
    ev = alg.evaluate(alg.eval_tasks[:n_paths], keep_paths=True)
    # provenance, so the demo can say how trained these weights are
    rows = json.loads((Path(run_dir) / "metrics.json").read_text())["metrics"]
    last_eval = [r for r in rows if "eval_final" in r][-1:]
    trained = dict(run=str(Path(run_dir).as_posix()), iterations=len(rows), of_iterations=cfg["num_iterations"],
                   env_steps=rows[-1]["env_steps"], eval_final=last_eval[0]["eval_final"] if last_eval else None)
    env = alg.env
    data = dict(
        env=cfg["env"], variant=cfg["variant"], latent=cfg["latent_size"], horizon=cfg["max_path_length"],
        num_exp_traj_eval=cfg["num_exp_traj_eval"], n_traj=int(np.ceil(cfg["num_steps_per_eval"] / cfg["max_path_length"])),
        sparse=env.sparse, use_next_obs=env.use_next_obs_in_context, goal_radius=getattr(env, "goal_radius", None),
        eval_tasks=[np.asarray(env.tasks[t]).tolist() for t in alg.eval_tasks],
        policy=dict(hidden=_mlp_layers(pol.fcs), mean=_mlp_layers([pol.last_fc])[0]),
        encoder=dict(hidden=_mlp_layers(enc.fcs), out=_mlp_layers([enc.last_fc])[0]),
        sample_paths=ev["paths"], trained=trained,
    )
    Path(out_file).parent.mkdir(parents=True, exist_ok=True)
    Path(out_file).write_text(json.dumps(data, separators=(",", ":")))
    print(f"wrote {out_file} ({Path(out_file).stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    export(*sys.argv[1:3])
