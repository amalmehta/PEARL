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

## Equations (`site/index.html` `.eq`, `site/js/math.js`, KaTeX 0.16.9)

- **Shows:** the five equations of the method: the product-of-Gaussians posterior (1) and its closed form (2), the KL bottleneck (3) and its closed form (4), and the critic loss that trains the encoder (5).
- **Why this way:** they're typeset like a paper, centred on the page and numbered, with no card around them. Cards made them look like the interactive widgets. A short sans-serif gloss under an equation defines any symbol the text hasn't. Notation is consistent throughout: `q_φ` everywhere, tasks written 𝒯, `\Vert` for the KL bars, full-size ½ in display.
- **Narrow screens:** equation numbers are hidden below 560 px, since the text never cites them and on a phone they collide with the right edge. Equation (4) has a two-line `data-tex-narrow` version that `math.js` swaps in.
- **Checked:** 2026-11-20 at desktop and 375 px widths, light and dark: no KaTeX errors and no equation scrolls sideways.
- **Changed:** 2026-11-20: cards removed, numbering added, the two halves of (2) merged into one line, notation unified, phone layout fixed.
