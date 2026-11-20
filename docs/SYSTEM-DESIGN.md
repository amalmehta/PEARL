# System Design

PEARL (Rakelly et al., ICML 2019) rebuilt from scratch. There are three parts: a Python package that trains and evaluates the algorithm, an experiment pipeline that turns runs into figures, and a static website that explains the method and runs a trained agent live in the browser.

## Architecture

```mermaid
flowchart LR
  subgraph py[pearl/ · Python + PyTorch]
    envs[envs.py<br>3 task families] --> trainer
    buffers[buffers.py<br>replay + encoder buffers] <--> trainer
    agent[agent.py<br>encoder q(z|c) + policy] <--> trainer
    trainer[trainer.py<br>collect · SAC+KL step · evaluate]
  end
  cfg[config.py<br>authors' hparams + budget] --> trainer
  trainer -->|metrics.json, agent.pt| runs[(runs/)]
  runs --> figs[make_figures.py] --> res[(results/summary.json<br>figures/*.png)]
  runs --> exp[export.py] --> data[(site/data/*.json)]
  res --> data
  data --> site[site/ · static HTML + JS<br>demo · charts · writeup]
  site -->|GitHub Pages| web((browser))
```

## Components

| Component | Job |
|---|---|
| `envs.py` | The 2D task families. Point-Robot and Sparse Point-Robot reproduce oyster's `point_robot.py`, including the seed-1337 task lists (checked by a test). Point-Wind is invented. |
| `gaussian.py` | Product of Gaussians (the posterior) and the KL to N(0, I). |
| `networks.py` | MLPs with rlkit's initialisation, the tanh-Gaussian policy, the permutation-invariant MLP encoder and the LSTM encoder. |
| `buffers.py` | Per-task ring buffers. `random_batch` gives shuffled transitions; `random_sequence` gives whole trajectories in order (for the RNN ablation). |
| `agent.py` | `infer` (context → posterior), `sample_z` (reparameterised), `act`. |
| `trainer.py` | The meta-training loop (oyster `rl_algorithm.train`), one SAC + encoder step (oyster `sac._take_step`), meta-test evaluation (oyster `collect_paths`). |
| `config.py` | `PAPER_DEFAULT` + `PAPER_ENV` copied from oyster's configs; `BUDGET` (laptop overrides); `VARIANTS` (ablations). |
| `experiments/` | A resumable parallel runner and the figure/aggregate generator. |
| `site/` | Static site. `model.js` reimplements the forward passes and the envs; the posterior is a running product updated per transition. |

## Main flows

1. **Meta-training** (`PEARL.train`). Collect initial data with z ~ prior for every training task. Then on each iteration: for a few random tasks, clear the encoder buffer and collect prior and posterior data. Then take N gradient steps, each on 16 tasks: context from the encoder buffer, RL batch from the replay buffer.
2. **One gradient step** (`train_step`). The encoder produces q(z|c) and z is sampled with gradients. The KL loss and the critic loss backpropagate into the encoder. V and the policy see z detached. The target V is soft-updated.
3. **Meta-test** (`evaluate`). On each held-out task, start from the prior and sample z per trajectory. After `num_exp_traj_eval` trajectories, refit q(z|c) on all context accumulated in the episode before each new trajectory. The policy acts deterministically.
4. **Results**. `make_figures.py` reads every `runs/*/*/seed*/metrics.json` and writes `results/summary.json`. The site's charts and result sentences are generated from that file, so no number is typed by hand.
5. **Resume**. After every iteration `_save_state` writes `state.pt`: all five networks, all five optimisers, both replay buffers (filled rows only), and the NumPy, environment and PyTorch random-number states. It writes to a temp file, then renames it, so a kill mid-save can't corrupt it. `train()` loads the file if its config and seed match, and continues. The iteration count alone may differ, so raising `num_iterations` trains a finished run further. A test checks that a resumed run's losses and returns are bit-identical to an uninterrupted run.
6. **Demo**. `export.py` writes the policy and encoder weights as base64 float32, plus where they came from (run, iterations trained, env steps, last held-out return), which the demo prints under the canvas. The browser decodes them once, then each step costs one policy pass plus one encoder pass, and the posterior update is O(latent).

## Where data lives

There are no servers, no accounts and no database. Raw runs are in `runs/` (git-ignored, regenerable), including each run's `state.pt` (a few MB to tens of MB, mostly the replay buffers). Committed aggregates are in `results/` and `figures/`, and the exported weights are in `site/data/`, a few hundred kB per family. The site keeps only viewer preferences, in `localStorage`, wrapped in try/catch.

## Key decisions and trade-offs

- **Hand-written 2D envs instead of Gymnasium.** Each is about 15 lines and needs no dependency, and the JS port is exact. Gymnasium would add nothing for these tasks.
- **CPU, PyTorch 2.2.2.** That is the last PyTorch with Intel-Mac wheels. Everything is small enough for CPU.
- **Faithful by default, budget made explicit.** Algorithmic hyperparameters are the authors' values. Only training length and width are cut (see below), and they are listed in one place.
- **Plain JS forward passes, not ONNX.** The networks are 3-layer MLPs. A 40-line forward pass loads instantly and needs no runtime.
- **Incremental posterior in the demo.** Because precisions add, each new transition costs one encoder call, not a re-encoding of the whole context. That keeps every frame well inside 16 ms.
- **Resume by saving everything, every iteration.** A stopped 12-hour suite used to throw away every partial run. Saving the full state each iteration costs well under a second, against 1–2 minutes per iteration. Saving every k iterations would be cheaper but loses up to k iterations on a stop.
- **The demo redraws only on change.** The canvas repaints only when a step, resize, theme or setting changes it, and the simulation pauses while it is scrolled off screen. Before, it repainted every frame forever.
- **Prose generated from the numbers.** `site/js/text.js` builds the result sentences from `summary.json`, so the writeup can't drift from the data.

## Deviations from the reference code

| What | oyster | Here | Why |
|---|---|---|---|
| LSTM hidden state at inference | carried across `infer_posterior` calls | reset each call, so the whole context is re-read | well-defined, and identical in training (mini-batch = batch) |
| Critic reward on sparse tasks | dense ("rewards are always dense") | dense (same) | kept for fidelity, flagged in the writeup |
| Buffer capacity | 1e6 per task | 1e5 per task | memory; never reached in these runs |
| GPU | optional | CPU only | laptop |

## Run budget

Algorithmic hyperparameters (learning rates, reward scale, KL weight, discount, latent size, data-collection schedule, evaluation protocol) are the authors' values. These are the only changes, all in `pearl/config.py` → `BUDGET`:

| Setting | Authors (oyster) | Here | Effect |
|---|---|---|---|
| Iterations | 500 | 150 (300 for sparse) | shorter training |
| Gradient steps / iteration | 1000 | 250 | 4× fewer updates per batch of data |
| Tasks per meta-batch | 16 | 8 | noisier gradients |
| RL batch per task | 256 | 128 | noisier gradients |
| Hidden width (policy, Q, V) | 300 | 128 | smaller function class |
| Context batch, sparse task | 1024 | 256 | noisier posterior during training |

**Why these numbers:** measured on this machine (Intel i9-9980HK, 8 cores / 16 threads, CPU only). One authors'-size step (16 × 256, width 300) took 398 ms at 2 threads; width 128 took 113 ms; halving the meta-batch and the batch cuts it about 4× again. A 40-iteration smoke run at this budget took dense Point-Robot from −24.8 (last trajectory, iteration 4) to −11.0 (iteration 29), still rising, which is why the suite runs 150 iterations.

**How long the suite takes (measured, not estimated).** An earlier note said about four hours. That was wrong. The first attempt (2026-10-20) ran 8 jobs in parallel at about 2 minutes per iteration on the slowest configurations (sparse Point-Robot, the RNN ablations), and stopped after about 47 of 150 iterations. On 2026-11-19, sparse Point-Robot's first iteration took 80 s with 8 jobs running. So the slowest runs take 3–5 hours each and the suite takes about 12 hours, depending on what else the machine is doing. `make status` prints the live figure. The full run on 2026-11-19/20 took 9 h 33 min (16:10 to 01:43). Other work kept the machine's load near 48, and the slowest runs took 4.9 h (RNN ablations) and 4.1 h (sparse Point-Robot).

**Reference lines in every figure:** *random actions* (uniform in [−1, 1]²) and an *oracle* that knows the task and steers straight at the goal at full speed, cancelling the wind. Both are computed by `make_figures.py` on the same 20 held-out tasks.

## Testing

`tests/test_core.py` contains:

- **Maths**: the product of Gaussians against a closed form and a brute-force density product on a grid; permutation invariance; that the posterior can only narrow; the KL against `torch.distributions`.
- **Envs**: the task lists equal oyster's seed stream; the sparse reward formula; action rescaling and clipping; wind dynamics.
- **Buffers**: trajectory sampling keeps order; ring-buffer wrap.
- **Algorithm**: every env × variant trains for 2 iterations; the encoder gets gradients from Q and not from the policy; more context gives lower posterior variance; seeded runs are bit-identical.
- **Resume**: a run stopped after 2 iterations and resumed to 4 matches an uninterrupted 4-iteration run exactly; a finished 2-iteration run extended to 4 matches too; a `state.pt` from a different seed or config is ignored.
- **Browser parity**: weights exported from a short run, then run through `site/js/model.js` in Node, give the same actions and posterior factors as PyTorch (to 1e-5), for an env with and without next_obs in the context.

What tests can't check is in `docs/MANUAL-REVIEW.md`.

## Known limits

- No MuJoCo, so the paper's headline numbers are cited, not reproduced.
- Short training and narrower nets (the run budget). Absolute returns are below what full-length training would give.
- 3 seeds give a rough spread, not a confidence interval.
- Point-Wind is invented, so there is no paper result to compare it with. It is also easy: the first trajectory, on a prior sample, already scores −4.84 against the oracle's −3.38, so it shows little adaptation.
- Sparse Point-Robot misses both of its done criteria (2026-11-20). Its mean last-trajectory return (1.93) is closer to random (0) than to the oracle (13.38). Checked per task with the final agents, it reaches the goal by the 5th trajectory on 4, 1 and 7 of 20 held-out tasks, where the bar was most of them. Returns were still rising slowly at iteration 150. Training it longer is the next thing to try, which needs `train()` to accept a higher iteration count on resume.
