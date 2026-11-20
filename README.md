# PEARL From Scratch

PEARL (Rakelly, Zhou, Quillen, Finn & Levine, ICML 2019), the off-policy meta-RL method that explores by sampling from a learned belief over tasks. Rebuilt here in plain PyTorch with no RL libraries, with an interactive explainer and a live in-browser demo.

![Three Gaussian factors, one per transition, and their product: the posterior over the task](docs/images/product-of-gaussians.png)

*Each transition casts a Gaussian vote on what the task is, and the belief is their product. That is why more evidence can only narrow it. This figure is interactive on the site.*

**Results** (3 seeds, last-trajectory return on 20 held-out tasks, full table in [`results/RESULTS.md`](results/RESULTS.md)):

- **Learns on dense Point-Robot** (−11.95 ± 1.19; random −21.08, oracle −4.49), only just past the halfway mark, and on Point-Wind (−3.98 ± 0.18; oracle −3.38).
- **Falls short on Sparse Point-Robot** (1.93 ± 1.01; random 0, oracle 13.38). It reaches the goal by the 5th trajectory on 4, 1 and 7 of 20 tasks, short of the paper's Fig. 7. The likely cause is the shortened training, but that is untested.
- **Ablations agree with the paper on z:** a deterministic z falls to random (−21.09). The RNN encoders come close to PEARL at about twice the cost per run.

- **Site:** [amalmehta.com/PEARL](https://amalmehta.com/PEARL/): writeup, demo, results
- [Instructions](docs/INSTRUCTIONS.md): setup, tests, training, reproducing every figure
- [System design](docs/SYSTEM-DESIGN.md): architecture, deviations from the authors' code, run budget, limits
- [File structure](docs/FILE-STRUCTURE.md) · [Manual review](docs/MANUAL-REVIEW.md) · [Viz log](docs/VIZ-LOG.md) · [Prompt log](docs/PROMPTS.md)
- Paper: [arXiv 1903.08254](https://arxiv.org/abs/1903.08254) · Authors' code: [katerakelly/oyster](https://github.com/katerakelly/oyster)

## How it was built

How this was built and how it works, with diagrams: [docs/HOW-IT-WAS-BUILT.md](docs/HOW-IT-WAS-BUILT.md)
