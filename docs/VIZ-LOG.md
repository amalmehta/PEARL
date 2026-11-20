# Viz Log

One entry per graphic on the site: what it shows, why it is drawn this way, the data behind it, and how it was checked.

## Live meta-test episode (`site/js/demo.js`, Canvas 2D)

- **Shows:** the trained agent on one held-out task. First it explores with z drawn from the prior, then it acts on posterior samples. Thin lines show where other samples from the current belief would take it.
- **Why a canvas:** the point is motion. You watch exploration narrow onto the goal step by step, which a static chart hides. It draws a few hundred line segments per frame, far below the point where WebGL would be needed.
- **Data:** weights exported by `pearl/export.py`. The environment dynamics are a direct port of `pearl/envs.py`.
- **Checked:** `test_browser_model_matches_torch` runs `model.js` in Node on exported weights and matches PyTorch to 1e-5. On 2026-11-19: screenshots in light and dark mode, and redraws now happen only on change, with the simulation paused off screen.
- **Changed:** 2026-11-19: the caption shows where the weights came from; draw-on-change; aria-live status line. 2026-11-20: weights re-exported from the finished seed-0 runs; the sparse-goal caption says that task falls short.

## Product of Gaussians (`site/js/figures.js` → `mountProduct`, SVG)

- **Shows:** three adjustable 1-D Gaussian factors and their exact product.
- **Why SVG:** few marks, crisp at any size, and it redraws on every slider input.
- **Data:** the closed form from `pearl/gaussian.py` (precisions add; the mean is precision-weighted).
- **Checked:** the readout's σ is always below the smallest factor's σ, matching `test_product_of_gaussians_is_permutation_invariant_and_narrows`. Screenshot used in the README, 2026-11-19.

## Results charts (`site/js/figures.js` → `chart`, SVG)

- **Shows:** learning curves, within-episode adaptation and ablations. Mean ± std across seeds, each seed drawn faintly, with random-action and oracle reference lines.
- **Data:** `site/data/summary.json`, copied from `results/summary.json` by `make export`.
- **Checked:** 2026-11-19, against a synthetic summary (9 charts and all result sentences render). With no summary, each group shows a single "Not run yet" note. 2026-11-20, against the finished suite: all charts render, and the sentences now say whether each family passes the "learns" check, computed from the same numbers.
