# Instructions

## Setup

Needs [uv](https://docs.astral.sh/uv/) and Python 3.11. PyTorch is pinned to 2.2.2, the last release with Intel-Mac wheels. It runs on CPU and needs no GPU.

```bash
make setup
```

## Check it works

```bash
make test
```

35 tests in about 35 seconds. They cover the product of Gaussians against a brute-force grid, the KL against `torch.distributions`, oyster's task lists, the sparse reward, buffer sequence sampling, that the encoder's gradient comes from the critic and not the policy, a short training run for every env × variant, seeded reproducibility, and that a stopped-then-resumed run, or a finished run trained further, gives exactly the same numbers as one that never stopped, and that the website's JavaScript networks give the same outputs as PyTorch on exported weights (needs Node.js; skipped without it).

## Train one run

```bash
.venv/bin/python -m pearl.train --env sparse_point --variant pearl --seed 0 --out runs/sparse_point/pearl/seed0
```

- `--env`: `point`, `sparse_point`, `point_wind`
- `--variant`: `pearl`, `deterministic`, `rnn_transitions`, `rnn_trajectories`, `ctx_offpolicy`, `ctx_rlbatch`
- `--paper-scale`: use the authors' iteration counts and network width instead of the laptop budget
- `--override '{"num_iterations": 5}'`: change any config key

The run writes `metrics.json` (config plus one row per iteration), `agent.pt` (the weights) and `state.pt` (everything needed to resume: networks, optimisers, replay buffers, random-number states) into `--out` after every iteration. Progress is logged every 5 iterations. If the run is stopped (a crash, a reboot, Ctrl-C), the same command picks up at the next iteration. Raising `num_iterations` (in `pearl/config.py` or with `--override`) trains a finished run further from where it ended.

## Reproduce every experiment and figure

```bash
make experiments    # 8 configurations x 3 seeds, ~12 h; resumes stopped runs, so it is safe to rerun
make status         # how far each run has got, its latest return, and a rough time left
make figures        # only rebuild results/ and figures/ from runs/
make export         # copy trained agents + results into site/data/ for the website
```

`make experiments` runs 8 jobs at a time with 2 threads each by default. Change that with `.venv/bin/python experiments/run_all.py --workers 4 --threads 4`. The log for each run is in `runs/<env>/<variant>/seed<k>/train.log`.

## The website

```bash
make site    # serves site/ at http://localhost:8431
```

The site is static: `site/index.html` plus JS modules and the JSON in `site/data/`. It is published on GitHub Pages from `site/` by the workflow in `.github/workflows/pages.yml`.

Using it:

- **Demo**: choose a task family, then click the canvas to move the goal (or set the wind). Watch the belief bars shrink and the returns rise after the exploration trajectories. The caption under the demo says which run the weights came from and how long it trained.
- **Results**: until `site/data/summary.json` exists, each chart says "Not run yet" rather than showing an empty box.
- **Settings**: the ⚙︎ button or ⌘, (Ctrl+, on other systems). Theme, demo speed, and whether to draw other samples from the belief.
- **Feedback**: the tab on the right edge opens a GitHub issue.
