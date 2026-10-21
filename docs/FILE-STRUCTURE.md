# File Structure

```
PEARL/
├── PEARL.md                  the project spec: answers, definitions, deferred items, changelog
├── README.md                 one-glance overview: figures and links
├── Makefile                  setup / test / experiments / figures / export / site
├── pyproject.toml            pinned dependencies (torch 2.2.2, numpy 1.26.4, matplotlib 3.8.4)
├── pearl/                    the algorithm, from scratch
│   ├── envs.py               Point-Robot, Sparse Point-Robot (oyster task lists), Point-Wind (invented)
│   ├── gaussian.py           product of Gaussians, KL to N(0, I)
│   ├── networks.py           MLP with rlkit init, tanh-Gaussian policy, MLP and LSTM encoders
│   ├── buffers.py            per-task ring buffers, transition and trajectory sampling
│   ├── agent.py              PEARLAgent: infer q(z|c), sample z, act
│   ├── trainer.py            meta-training loop, SAC + encoder step, meta-test evaluation
│   ├── config.py             authors' hyperparameters, laptop budget, ablation variants
│   ├── train.py              CLI for one run
│   └── export.py             trained agent -> JSON (base64 float32) for the browser demo
├── experiments/
│   ├── run_all.py            the whole suite, in parallel, resumable
│   └── make_figures.py       runs/ -> results/summary.json, results/RESULTS.md, figures/*.png
├── tests/test_core.py        unit and integration tests
├── results/                  committed aggregates (small JSON + Markdown table)
├── figures/                  committed PNG figures used by the README
├── runs/                     raw per-run logs and checkpoints (git-ignored)
├── site/                     the static website (GitHub Pages)
│   ├── index.html            the Distill-style writeup with the demo and charts
│   ├── style.css             warm light theme + dark theme tokens
│   ├── icon.svg              app icon / favicon
│   ├── mockups.html          the three layout mockups (A was chosen)
│   ├── js/model.js           policy, encoder, posterior and envs in plain JS
│   ├── js/demo.js            the interactive meta-test episode
│   ├── js/figures.js         product-of-Gaussians figure and results charts
│   ├── js/text.js            result sentences generated from summary.json
│   ├── js/settings.js        settings dialog (⌘,)
│   └── data/                 exported agents and summary.json
├── docs/
│   ├── INSTRUCTIONS.md       setup, run, use
│   ├── SYSTEM-DESIGN.md      architecture, decisions, deviations, testing, limits
│   ├── FILE-STRUCTURE.md     this file
│   └── MANUAL-REVIEW.md      checklist for what tests can't check
└── .github/workflows/        tests on push; publish site/ to Pages
```
