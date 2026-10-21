PROJECT NAME: PEARL

META-INSTRUCTIONS:

<Read it all before acting. Ask about anything unclear, contradictory or
 underspecified — before starting and mid-build. Ask in the question widget
 (AskUserQuestion): related questions batched, concrete options, your
 recommendation first. Plain text only if the widget isn't available.>

<Make answering easy. Before building, pick my brain about what it's really
 for and who for, what would make it great rather than fine, examples I love or
 hate, and what I've tried before — but mostly through the question widget: give
 each question 2–4 likely answers to pick from (several may apply), so I can
 click one or type my own in the box. Only when a question needs a fleshed-out
 answer that options can't capture (describe the person, paste an example, give
 detailed instructions) ask it in plain text, as one short question with a line
 on what a good answer covers, at most two per round. Never a long numbered list
 of open questions. Wait for my answers and follow up where they open something
 up.>

<Don't expand scope. Anything not listed here is a proposal, including changes
 to this file — propose it, don't do it.>

<Prefer doing over describing: run the code, write the files, test it.>

<As soon as a first working version (the MVP) exists, open it for me before
 carrying on: launch the app, open the page in the browser, or run it on a real
 sample, and say in a line or two what to try. Do the same after each big change.>

<Always in scope, no proposal needed: when it goes on GitHub, a README that is
 easy to read at a glance — a line on what it is, then clear visuals
 (screenshots, a diagram or a chart), then links. Everything else goes in
 linked files: docs/INSTRUCTIONS.md (setup, run, use),
 docs/SYSTEM-DESIGN.md (see below) and docs/FILE-STRUCTURE.md (what's where). If what you're
 building is an application rather than a script, also a small unobtrusive feedback tab, and a settings
 button or tab (⌘, on the Mac) that gathers its preferences in one place.>

<If what you're building is an application and the request names no platform,
 build it as a Mac app first; the website comes after, as its own step. If it
 names a platform or implies a different deliverable, follow that, and ask
 before applying this default.>

<Always create a relevant icon for applications: one that says what the app
 is at a glance, used everywhere it shows up (Dock or home screen, the website's
 favicon, notifications).>

<Never let anything made up pass as fact: check computed or generated facts
 against real sources and cite them, and label estimates, assumptions and
 invented parameters as such in the UI and the docs.>

<Fill in DEFINITIONS AND DEFERRED in this spec before building: give every
 vague term a threshold, formula or done criterion, and list what's left for
 later.>

<Keep the interface clean and restrained: a warm, light palette with sparing
 accents, and dark mode checked on every component. When the visuals are open-
 ended, offer two or three mockups to pick from. Finish with a manual review
 checklist for what tests can't check: feel, hardware, live services.>

<Make it buttery smooth; this is a priority, not polish. Every tap, click and
 keystroke answers at once (under 100 ms): show the change right away and do
 the slow work after. Never block the main thread: files, network, parsing and
 heavy work run in the background. Keep motion at the display's full frame
 rate, with short eased transitions (about 150–250 ms) for things that appear,
 move or change, and no flicker, jumps or layout shifts. Show the last known
 content while refreshing instead of an empty screen or a spinner, keep long
 lists lazy and scrolling fluid, and debounce work that follows typing.
 Profile the slowest interactions before calling it done, and add smoothness
 to the manual review checklist.>

<Work like a world-class founder: start from one real person and the problem
 they have now, and name the one result that would make this worth it. Build
 the smallest version that delivers it, put it in front of them early, and let
 what they do (not what's easy to build) decide what comes next. Cut what
 doesn't serve that result, and note cost, distribution and who pays.>

<Work like a world-class software engineer: choose the simplest design that
 will hold, and the boring proven tool over the clever one. Make it correct
 first, with tests for the behavior that matters and edge cases handled; keep
 changes small and reversible; measure before optimizing; secure by default
 (no secrets in the repo, least privilege); log what will help debug it; and
 record the key decisions and trade-offs in docs/SYSTEM-DESIGN.md.>

<For research, work like a world-class scientist: read what's already known
 before building, then state the question, hypothesis, baseline and metric
 before running anything. Change one thing at a time with controls and
 ablations; use several seeds and report variance; keep it reproducible
 (pinned versions and data, one command regenerates every figure); keep
 exploration separate from confirmation; and report negative results and
 limits as plainly as wins.>

<Before building, ask the design questions an expert software engineer would
 for this project: where data lives (database, schema, sync, backups), auth and
 security (who can see or change what, secrets and keys), caching and
 performance, scale and concurrency, offline behavior, privacy, error handling,
 deployment and cost. Include delivery in the same first batch: the
 deliverable's form, platforms and minimum OS versions, signing and
 distribution, and the repo (who creates it, public or private, push or only
 commit locally). For paid or external services, ask about test versus live
 mode and who pays, and offer a mock mode. Ask for real sample inputs and
 working credentials before building. Batch them in the question widget, each
 with your recommendation first; skip what clearly doesn't apply, and record
 the answers in the spec.>

<When an application takes files as input, offer a visible Upload button that
 opens the file picker, accept files dragged anywhere onto the window (not
 only onto a small drop zone), and accept pasting them with ⌘V.>

<Color-code tags, categories and types by similarity: related ones share a
 hue family, with shades far enough apart to tell them apart at a glance, in
 both light and dark mode.>

<Name things the way a person would say them — "Goal Tracker", not
 goal_tracker — for the app, its windows, titles, files people open, repo
 descriptions and README headings. When you create the GitHub repo, name it
 with no "_" or "-": one word or joined words, e.g. GoalTracker.>

<Always in scope: a system design doc in the codebase, docs/SYSTEM-DESIGN.md,
 kept current as the build changes. Cover the architecture (with a Mermaid
 diagram), each component's job, the main flows, where data lives, the key
 design decisions and their trade-offs, how it's tested, and known limits.>

<Finish by listing every deliverable: path, what it is, how to check it works.>

<Git rules (no Claude attribution, never commit .claude/) are in
 ~/.claude/CLAUDE.md and apply on their own — nothing to repeat here.>

<Keep the changelog at the bottom current.>

FROM SIMILAR PAST PROJECTS:

<The closest earlier projects by meaning, each with one concrete thing it settled. Examples to learn from, not choices to copy.>

<autonomous_driving_sim (website, 73% alike): assumed: Agent fills in: what it guessed, what it decided without asking.>

LEARNED ACROSS PROJECTS:

<What held across several kinds of earlier projects: starting points, not rules.>

<Decide which data sources, external services and licenses are allowed, test versus live mode, key storage, who pays, spending limits, privacy, and offline behavior. (across 12 kinds)>

<Settle the deliverable's form, target platforms, minimum versions and distribution up front, including packaging, signing, hosting and who runs it. (across 11 kinds)>

<Define vague terms, scope boundaries and scoring rules with concrete thresholds, formulas and done criteria, recording what is deferred. (across 9 kinds)>

<Validate generated or computed content against real sources, cite them, and label estimates or invented parameters so nothing fabricated passes as fact. (across 8 kinds)>

<Settle version control policy early: who creates and hosts the repository, its visibility, and whether to push or only commit locally. (across 7 kinds)>

<Gather real sample inputs and working credentials early, then verify live APIs, model output and system tools, keeping a fallback ready. (across 7 kinds)>

<Define each output's specs, tone and visual style before building, offering a few concrete concepts or mockups to pick from when open-ended. (across 6 kinds)>

<Plan a manual or human review checklist for what automated tests can't verify, such as hardware, live services, feel or taste. (across 3 kinds)>

LEARNED FOR PAPER REIMPLEMENTATION / STUDY PROJECTS:

<Starting points from 11 earlier paper reimplementation / study projects, not rules: use what fits this one, and ask when it differs.>

<Ask which paid APIs, accounts, repositories and hosting the user will provide, who pays for model calls, and where keys, secrets and data live. (seen in 10)>

<Settle target platform, OS version, deliverable type, packaging and signing, deploy timing and code location, especially when the brief conflicts with standing defaults. (seen in 8)>

<Settle which paper version, reference sources, datasets and content assets to use, verify values at primary sources, and define what 'from scratch' allows. (seen in 5)>

<Settle the demo's form, which model or engine powers it, where compute runs, offline fallbacks, default libraries, and budget; reference hyperparameters may be too slow interactively. (seen in 5)>

CONTEXT:

Project type: Paper reimplementation / study (reproducing or studying a paper's method, checked against its reported results).

completely recreate pearl from scratch, along with a writeup, demo, experiements, in various types of environemnts

DELIVERABLES:

website + experiements + demo + writeup

DEFINITIONS AND DEFERRED:

- PEARL = Rakelly, Zhou, Quillen, Finn, Levine, "Efficient Off-Policy Meta-Reinforcement
  Learning via Probabilistic Context Variables", ICML 2019, arXiv 1903.08254. Reference
  implementation for checking details: github.com/katerakelly/oyster (configs/default.py,
  configs/point-robot.json, configs/sparse-point-robot.json, rlkit/torch/sac/{agent,sac}.py).
- "From scratch" = PyTorch 2.2.2 + NumPy only. SAC (twin Q, V, target V, tanh-Gaussian
  policy), context encoder, product of Gaussians, KL, replay buffers, samplers, the
  meta-training loop and evaluation are all hand-written. No RL library. The 2D environments
  are hand-written too (a few lines each), so Gymnasium is not needed and is not a dependency.
- "Faithful" = every hyperparameter equals the oyster config for that env unless it is listed
  in the run-budget table in docs/SYSTEM-DESIGN.md, which marks each change as a laptop-budget
  deviation. The budget cuts training length, meta-batch (16→8 tasks), RL batch (256→128) and
  width (300→128). Nothing algorithmic changes.
- Reference lines: "random actions" (floor) and "oracle" (knows the task, steers straight at the
  goal at full speed). Both are computed, not assumed, by experiments/make_figures.py.
- Environments ("various types"):
  1. Point-Robot (dense): oyster `point-robot`. Goals uniform in [-1,1]^2, reward = -||x-g||,
     actions in [-0.1,0.1]^2, horizon 20. In the paper's code, not reported in the paper.
  2. Sparse Point-Robot: oyster `sparse-point-robot`. Goals on a radius-1 half circle, reward
     only within radius 0.2, horizon 20. This is the paper's Fig. 7 exploration task.
  3. Point-Wind (dynamics vary): NOT in the paper, invented for this project and labelled
     that way everywhere. Fixed goal at the origin, per-task wind w ~ U[-0.05,0.05]^2 added
     to every step, next_obs included in the context.
- "Matches the paper" (done criterion): sparse Point-Robot with PEARL beats the
  prior-only first trajectory and reaches the goal radius by trajectory <= 5 of evaluation on
  most eval tasks, qualitatively as in Fig. 7. The paper gives no point-robot numbers, so this
  check is qualitative and is labelled as such. The paper's MuJoCo numbers are cited as
  "reported, not reproduced".
- Ablations (paper Sec. 6.3, run on dense Point-Robot): (a) probabilistic vs deterministic
  z; (b) permutation-invariant MLP encoder vs RNN on shuffled transitions vs RNN on
  trajectories; (c) context sampling from recent data (PEARL) vs the whole replay buffer
  vs the same batch as the RL batch.
- "Learns" (done criterion): the PEARL mean last-trajectory return on each family ends closer to
  the oracle than to random actions.
- Seeds: 3 per configuration. Report mean ± std across seeds and show each seed faintly.
- Run budget: the whole suite runs from one command (`make experiments`) in a few hours on
  the 16-thread Intel i9 CPU.
- Demo done criterion: in the browser, pick or click a goal and the trained policy runs
  live in JS from exported weights. You see exploration trajectories and the posterior's
  variance shrink as context accumulates. Every step renders within a 16 ms frame.
- Smooth: input feedback < 100 ms; animations at display rate; transitions 150–250 ms ease;
  no layout shift (fixed-size canvases); inference stays inside the frame budget, which is
  measured and reported in the manual review checklist.
- Site = static, Distill-style article on GitHub Pages: writeup + interactive figures +
  demo + results charts. Has a settings panel (theme, demo speed, show samples),
  a small feedback tab (opens a GitHub issue) and a favicon/icon.
- Deferred: MuJoCo tasks (Half-Cheetah, Ant, Humanoid, Walker), plain SAC baseline,
  MAML/RL²/ProMP baselines, GPU runs, Mac app (the spec's default, replaced by a
  static site at the user's choice), paper-scale iteration counts.

OPEN QUESTIONS / ASSUMPTIONS:

- Answers recorded 2026-10-20: paper = meta-RL PEARL; purpose = learn it deeply,
  portfolio, research baseline and teaching; compute = laptop only; demo = static site + in-browser
  demo; envs = several cheap 2D families; ablations = the paper's; repo = public "PEARL"
  created by Claude with gh and pushed, site on GitHub Pages; scratch = PyTorch, no RL libs;
  budget = a few hours, 3 seeds; style = Distill-style article. The user tried PEARL before:
  the method didn't click, training didn't work, and the original code was hard to use. So the
  writeup explains each term, and each piece has its own test.
- Data/auth/backups/cost: none apply. Static site, no accounts, no server, no paid services.
  Results are committed as small JSON; checkpoints are git-ignored except the exported demo
  weights.
- Assumed: oyster's sparse Point-Robot trains the critic on DENSE rewards (sample_sac
  "rewards are always dense") and gives only the encoder sparse rewards. Kept as the default
  to stay faithful, and flagged in the writeup.
- Assumed: Gymnasium dropped (see "from scratch") because the envs are tiny.
- Assumed: Python 3.11 + torch 2.2.2, the last PyTorch with Intel-Mac wheels.

CHANGELOG:

- 2026-10-20 — created
- 2026-10-20 — filled in definitions, deferred items and answers; set the laptop run budget after timing (machine load forced a 4x cheaper step); added random and oracle reference lines
- 2026-09-15 — added meta-instruction: built-out applications include a small feedback tab
- 2026-09-15 — added meta-instruction: no "Claude" attribution in commits, PRs, or branches
- 2026-09-16 — added meta-instruction: always include a README when adding to GitHub
- 2026-09-16 — changed meta-instruction: ask clarifying questions in the question widget
- 2026-09-17 — added meta-instructions: Claude never a contributor; never commit .claude/
- 2026-09-26 — compressed the meta-instructions and every field prompt; git rules moved to the global instruction file
- 2026-09-27 — added meta-instruction: applications are built as a Mac app first, then a website
- 2026-09-28 — folded inputs, instructions, constraints, deliverables and done criteria into one free-form CONTEXT
- 2026-09-28 — changed meta-instruction: a README on GitHub always includes a visual
- 2026-09-28 — added meta-instruction: name things like a person would, never snake_case
- 2026-09-28 — changed meta-instruction: README leads with visuals; instructions live in a linked guide
- 2026-09-28 — changed meta-instruction: README is visuals and links; details in docs/INSTRUCTIONS.md and docs/FILE-STRUCTURE.md
- 2026-09-29 — changed meta-instruction: GitHub repo names have no "_" or "-"
- 2026-10-02 — added a DELIVERABLES field after CONTEXT
- 2026-10-02 — added meta-instruction: every project has a system design doc at docs/SYSTEM-DESIGN.md
- 2026-10-05 — added meta-instruction: applications include a settings button or tab
- 2026-10-08 — added meta-instruction: color-code tags by similarity (related share a hue family, each distinct)
- 2026-10-09 — added meta-instruction: apps that take files have an Upload button, drop anywhere, and paste
- 2026-10-17 — added meta-instruction: before building, ask the design questions an expert engineer would (data, security, caching, scale, deployment…)
- 2026-10-18 — added meta-instruction: open the MVP for me as soon as a first working version exists, and after each big change
- 2026-10-18 — added meta-instruction: always create a relevant icon for applications
- 2026-10-18 — added meta-instructions: work like a world-class founder, software engineer and (for research) scientist
- 2026-10-18 — added meta-instruction: pick my brain with open questions answered in my own words, as well as multiple choice
- 2026-10-18 — changed meta-instruction: Mac app first only when the request names no platform (from the meta report)
- 2026-10-18 — changed meta-instruction: the first batch of questions also covers delivery, the repo, test versus live mode, who pays, mocks, and real inputs and credentials (from the meta report)
- 2026-10-18 — added meta-instructions: nothing made up passes as fact; fill in DEFINITIONS AND DEFERRED; a clean, restrained interface with mockups and a manual review checklist (from the meta report)
- 2026-10-18 — added a DEFINITIONS AND DEFERRED section
- 2026-10-19 — changed meta-instruction: questions mostly as multiple choice (with a box for my own answer); plain-text questions only when a detailed answer is needed, at most two per round
- 2026-10-20 — added meta-instruction: make the UI/UX buttery smooth (instant response, nothing blocking the main thread, full-frame-rate motion, no flicker or jumps)
