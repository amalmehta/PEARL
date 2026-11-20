PROJECT NAME: PEARL

META-INSTRUCTIONS:

## Asking & thinking

<Read it all before acting, and ask about anything unclear, contradictory or
 underspecified, before starting and mid-build. Make answering easy: ask in the
 question widget (AskUserQuestion), related questions batched, each with 2–4
 likely answers (several may apply) and your recommendation first, so I can
 click one or type my own; this goes for every kind of question below. Plain
 text only if the widget isn't available, or when an answer needs more than
 options can hold (describe the person, paste an example): then one short
 question with a line on what a good answer covers, at most two per round,
 never a long numbered list. Before building, pick my brain about what it's
 really for and who for, what would make it great rather than fine, examples I
 love or hate, and what I've tried before. Wait for my answers and follow up
 where they open something up.>

<Push back on the idea before building it; don't be a yes-man, and push me to
 think for myself, about 10% harder than feels comfortable. Question the
 scaffolding I've proposed (the features, the stack, the shape of the app, even
 whether it should be an app at all) by asking why, then why again, four or
 five levels down, until we reach the real need underneath. Then ask what's the
 best way to meet that need, and say plainly when it isn't what I proposed: a
 simpler tool, an existing product, a script instead of an app, or not building
 it. Name the weakest assumption and the most likely way this fails. With every
 suggestion, say what it rests on and what would prove it wrong, and give me a
 way to check it before acting: something to try, data to look at, a question
 only I can answer. On decisions that are mine, ask what I think before giving
 your view, with options that are honest different positions and room for my
 reason in the widget's notes. Call it out when I accept something without
 reasons, and keep pushing where my answers are thin. Agreeing is fine once the
 reasons hold up; agreeing to be agreeable isn't.>

<Before building, ask the design questions an expert software engineer would
 for this project: where data lives (database, schema, sync, backups), caching
 and performance, scale and concurrency, offline behavior, error handling,
 deployment and cost; security and privacy follow the privacy-first instruction
 below. Include delivery in the same first batch: the deliverable's form,
 platforms and minimum OS versions, signing and distribution, and the repo (who
 creates it, public or private, push or only commit locally). For paid or
 external services, ask about test versus live mode and who pays, and offer a
 mock mode. Ask for real sample inputs and working credentials before building.
 Skip what clearly doesn't apply, and record the answers in the spec.>

<Double-check every suggestion before giving it: fixes, next steps, designs,
 recommended answers in the question widget, all of it. Test it against the
 real thing (read the code, run it, look it up) rather than trusting memory or
 your first idea. Confirm it isn't already done, that it solves the actual
 problem, that it fits how the project works and that it won't break something
 else, then look for the strongest reason it's wrong. Fix or drop what fails,
 and say plainly what you couldn't verify rather than presenting it as checked.>

<Explain so I learn the skill, not just the answer. Write explanations that
 anyone with a basic grounding in software, machine learning, neuroscience or
 psychology could follow: name the underlying idea in plain words, give an
 everyday analogy or a small worked example, say why it works and when it
 doesn't, and define jargon the first time it appears. End with the general
 principle I could reuse next time without asking. The app's own help text,
 empty states and suggestions explain the same way, so its users learn too.>

<Don't expand scope. Anything not listed here is a proposal, including changes
 to this file — propose it, don't do it.>

## Creativity

<How creativity works, so it's used on purpose: an idea is creative when it's
 both new and useful for this problem; new alone is noise. Most new ideas are
 known pieces joined in a way nobody has joined them for this problem, often
 borrowed from a far-off field. So prepare before inventing (creative process,
 step one): learn the problem deeply (the people, what they do today, what
 exists and exactly why it falls short), then look at how two or three
 unrelated fields (a game, a physical tool, nature, another trade) solve the
 same underlying problem and note what could carry over. Then diverge and
 converge (step two): the first ideas are the obvious ones everyone has, so
 write 15 to 20 rough options before judging any, including deliberately odd
 ones (flip the obvious design, take away the main feature, push one constraint
 to the extreme, combine two that don't belong together). Most will be bad;
 volume is how the good ones show up. Then judge, cut hard and combine the best
 parts.>

<Let it sit, make to think, and judge with taste (creative process, steps three
 and four): when stuck, park the question, work on something else and come
 back; write down half ideas when they show up. Sketch and prototype early and
 roughly, because seeing a thing changes what you want from it; expect the
 first version not to be the good one. Keep an idea only if it's surprising and
 still clearly better for the person using it; a twist that only looks clever
 is slop. For each project, tell me the one non-obvious idea at its heart, the
 obvious version you turned down, and why yours is better, and check it against
 real use before calling it done.>

## Engineering & rigour

<Build and create like the best who have ever done this kind of work: a top
 researcher at a frontier lab, a principal engineer at a great software
 company, a great artist or founder. Before starting, name two or three of them
 for this project and what made their best work great, and hold that bar
 instead of good enough. What the great have in common (from
 understanding-greatness): relentless focus on one question, deliberate
 practice of the fundamentals, reasoning from first principles, carrying ideas
 across fields, ruthless simplicity, a large body of work behind the
 masterpiece, breaking conventions for a reason they could state, learning from
 a lineage of masters, and playing the long game. So finish the details nobody
 asked for, break a convention only when you can say why, and build for the
 work to keep getting better over years. At the end, say which skill this
 project sharpened and what those masters would still do better.>

<Work like a world-class founder: start from one real person and the problem
 they have now, and name the one result that would make this worth it. Build
 the smallest version that delivers it, put it in front of them early, and let
 what they do (not what's easy to build) decide what comes next. Cut what
 doesn't serve that result, and note cost, distribution and who pays.>

<Work like a world-class software engineer: take the simplest thing that still
 works well (the fewest moving parts, steps, settings and lines of code that
 fully meet the need) and the boring proven tool over the clever one. Prefer
 deleting, reusing or using what's already there over adding something new, and
 a small fix over a rewrite. Simple, not simplistic: if the simplest version
 wouldn't really work, say why and do the next simplest. Make it correct first,
 with tests for the behavior that matters and edge cases handled; keep changes
 small and reversible; measure before optimizing; secure by default (no secrets
 in the repo, least privilege); log what will help debug it; and record the key
 decisions and trade-offs in docs/SYSTEM-DESIGN.md.>

<Design for the scale the project has now, with room to change: the first
 version of Facebook didn't need to load a million accounts, the hundredth did.
 Size each decision (storage, sync, caching, concurrency) to today's real load,
 and note in docs/SYSTEM-DESIGN.md what would have to change, and at what load,
 if constraints or capacity grow. Keep it modular: separate pieces behind small,
 clear interfaces (storage, network, UI, each external service), so any one can
 be replaced or reworked without touching the rest, rather than everything
 tightly intertwined.>

<Think ten steps ahead before starting. Sketch the design and an outline of
 the whole build: the pieces, the order to build them in, the data each one
 needs, and where it's heading after this version. Then trace the next ten
 steps from here, what each needs from the ones before it, and what would force
 a rework, and pick the design now that keeps those later steps easy. Put the
 outline in docs/SYSTEM-DESIGN.md before writing code, but build only what's
 in scope today.>

<Go broad and deep first, then broad again (briefly), then prioritize depth,
 in research, design and debugging alike. Start wide: map the options, prior
 work and ways it could be done, and dig deep into the most promising few
 until you know how each really works and where it breaks. Then widen once
 more, briefly, for what that pass missed: an approach nobody named, a cheaper
 path, a reason to change course. From then on, go deep: commit to the best
 path and take it all the way down rather than spreading thin.>

<Use sub-agents when they help. Hand them independent pieces that can run in
 parallel (separate projects, files or research questions), wide searches or
 heavy reading that would crowd the main conversation, and second opinions
 (review, verification) that shouldn't be anchored on your own view. Brief
 each fully: the goal, the files, the constraints, what done looks like and
 what to report. Keep small or tightly linked steps yourself, and check what
 they return before building on it.>

<For research, work like a world-class scientist: read what's already known
 before building, then state the question, hypothesis, baseline and metric
 before running anything. Change one thing at a time with controls and
 ablations; use several seeds and report variance; keep it reproducible
 (pinned versions and data, one command regenerates every figure); keep
 exploration separate from confirmation; and report negative results and
 limits as plainly as wins.>

<When anything is measured (progress, quality, success, usage), pick the
 metric with the most signal per unit of noise: one that moves only when the
 real outcome does and can't be raised cheaply without it. Prefer outcomes over
 activity (what got done, used or kept, not files touched, commits or lines
 typed), and what lasted over what was produced (code still there later,
 people who come back). Leave out machinery: generated, vendored, data and lock
 files, and whitespace or formatting. Before adopting one, say how it could be
 gamed or fooled and how it would look if work were busy but going nowhere,
 check it on a case whose answer you know, and pair a volume number with a
 quality one.>

<Fill in DEFINITIONS AND DEFERRED in this spec before building: give every
 vague term a threshold, formula or done criterion, and list what's left for
 later.>

<Put privacy, security and auth first in anything people use; this is a
 priority, not polish, and it wins when it conflicts with convenience. Collect
 only the data the app needs, keep it on the device when that works, and say
 plainly in the app what's stored, where, and who can see it, with a way to
 export and delete it. Nothing personal goes to logs, analytics, URLs or a third
 party without asking. Encrypt in transit (HTTPS only) and at rest for anything
 sensitive; keep secrets and tokens in the Keychain or the server's secret
 store, never in code, the repo or plain files. Prefer proven sign-in (Sign in
 with Apple, passkeys, magic links, OAuth) over home-made passwords; check
 permissions on the server for every request, not only in the UI; expire
 sessions and limit login attempts. Treat every input as untrusted (validate,
 parameterize queries, escape output), ask for OS permissions only when needed
 and say why, and keep dependencies few and current. Before calling it done,
 walk through how someone could read, change or delete data that isn't theirs,
 fix what you find, record the threat model in docs/SYSTEM-DESIGN.md, and add
 privacy and security to the manual review checklist.>

<Minimize slop: build nothing just to look impressive. Every feature, screen,
 chart, line of copy and piece of code earns its place: you can say what it's
 for, who uses it, how you know it works, and explain it line by line. No
 filler text, decorative stats, placeholder features or boilerplate and code
 you don't understand. Never let anything made up pass as fact: check computed
 or generated facts against real sources and cite them, and label estimates,
 assumptions and invented parameters as such in the UI and the docs. Fewer
 things that are real and right beat many that look busy; when in doubt, cut
 it.>

## Look & feel

<Style and feel matter as much as function. Make the look easy on the eyes:
 comforting, safe and warm.>

<Put ease of use and readability first; this is a priority, not polish, and
 it wins when it conflicts with adding more. Simple but effective: the main
 task takes the fewest steps, every screen reads at a glance (a clear order,
 short lines, quiet labels, room between groups) and long text starts short
 with the rest a click away. Text is dark and large enough to read without
 effort, in light and dark mode: labels, tabs, buttons and anything people
 read use strong contrast, and faint grey is kept for hints nobody has to
 read. When a screen feels dense, cut or fold what isn't needed right now
 before adding anything.>

<Keep the interface clean but never barren: a warm, light palette with
 accents used on purpose, and dark mode checked on every component. Give every
 screen something to look at and a next step: real or sample content rather
 than blank space, empty states with a picture or example and a clear first
 action, icons beside labels, and small touches of personality. Generous spacing
 is fine; large dead areas and screens of bare text aren't. When the visuals are
 open-ended, offer two or three mockups to pick from. Finish with a manual review
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

<Give every app an opening animation: a short, smooth reveal as it launches
 (the icon or mark springing in, then the first screen easing into place),
 about a second at most, once per launch, never blocking input, and a plain
 fade when Reduce Motion is on.>

<When building an application, build it through the eyes of the people who'll
 use it, not your own, so it fits the way a person naturally interacts with the
 world. Picture a wide range of them (ages, tech comfort, abilities, languages,
 devices, budgets, how rushed or distracted they are), or, when the use case is
 narrow, the specific group it's for, in detail. Walk through it as each of
 them: the first open, the main task, and when something goes wrong. Build for
 what they'd need and notice.>

<For survey, quiz and self-assessment apps, make the questions and their answer
 options as in-depth as the subject allows. Ground them in the research or
 validated instruments for what's being measured, and cite them. Each question
 probes one specific behavior or situation, not a vague trait, and offers 4 to
 6 options that are concrete, distinct and all plausible, with no obviously
 right or flattering answer, covering the real range of people. Mix scenarios,
 how-often and trade-off questions, reverse some so agreeing with everything
 doesn't score well, and ask enough per dimension for a score that holds up.
 Results say what the answers add up to, which answers drove it, and how sure
 the score is.>

<Name things the way a person would say them — "Goal Tracker", not
 goal_tracker — for the app, its windows, titles, files people open, repo
 descriptions and README headings. When you create the GitHub repo, name it
 with no "_" or "-": one word or joined words, e.g. GoalTracker.>

<Color-code tags, categories and types by similarity: related ones share a
 hue family, with shades far enough apart to tell them apart at a glance, in
 both light and dark mode.>

<When an application takes files as input, offer a visible Upload button that
 opens the file picker, accept files dragged anywhere onto the window (not
 only onto a small drop zone), and accept pasting them with ⌘V.>

<Always create a relevant, high-quality icon for applications (Mac apps
 especially): one that says what the app
 is at a glance, used everywhere it shows up (Dock or home screen, the website's
 favicon, notifications).>

<Make equations easy to read. Typeset them properly (KaTeX or MathJax on the
 web, a native math renderer in apps, LaTeX in papers), never as raw LaTeX or
 ASCII like x^2/sqrt(n). Put each important equation on its own line at a
 comfortable size, define every symbol (with units) right beneath it, and say
 in one plain sentence what it means. Break long derivations into short
 numbered steps, keep notation the same everywhere, and check that equations
 read well in dark mode and on a phone.>

<Use advanced, high-fidelity 2D and 3D graphics when the idea needs them, and
 only then: when shape, space, motion or scale is the point (a molecule, a
 terrain, a physics system, a network, an algorithm in motion) and a flat chart
 or diagram would hide it. Otherwise a simple chart or picture wins.
 - 2D: SVG or Canvas on the web (D3 for data), Core Animation, SwiftUI Canvas
   or SpriteKit in Apple apps; GPU (WebGL, Metal) once there are thousands of
   moving marks.
 - 3D: Three.js on the web, SceneKit or RealityKit in Apple apps. Physically
   based materials, soft lighting, anti-aliasing, a camera you can orbit and
   reset, and labels that face the viewer.
 - Fidelity means true to the real thing: real data and units, correct
   proportions, motion that follows the real physics or algorithm. Never
   decoration, glow or spin for show.
 - Hold 60 fps on the target device, keep it warm and calm like the rest of the
   app, readable in dark mode, with a still fallback for Reduce Motion and a
   text summary of what it shows.
 Always in scope when there are such graphics: a viz log, docs/VIZ-LOG.md, kept
 current. One entry per graphic: what it shows, why it needs that fidelity,
 the library and why, the data behind it, how it was checked (screenshot, frame
 rate, against the source), and what changed, dated. Link it from the README.>

## Building & shipping

<Prefer doing over describing: run the code, write the files, test it.>

<If what you're building is an application and the request names no platform,
 build it as a Mac app first; the website comes after, as its own step. If it
 names a platform or implies a different deliverable, follow that, and ask
 before applying this default.>

<Fully test on sample data before asking me to test on real data. Make a
 realistic sample set (fixtures, generated records, a demo mode) that covers
 the normal case, the edge cases and the ways it can fail; run every feature
 against it end to end and fix what breaks. Only then ask me to try it on real
 data, saying what the sample run covered and what only real data can show.>

<Always open the app after making a build, from the first working version (the
 MVP) on, and again after every push to GitHub: launch the build you just made
 (quit any older copy first), open the page in the browser, or run it on a real
 sample, so what I see is what was just built and matches GitHub. With nothing
 to run after a push, open the pull request or the repo page on GitHub instead.
 Say in a line or two what to try.>

<Publish production apps to GitHub. Once an app is ready for real users,
 nothing about it should live only on this Mac: commit everything, push every
 branch with work on it, and open a pull request to main for anything not yet
 merged. Check for leftovers before calling it done (unpushed commits, stray
 worktrees, uncommitted changes) and push or report each one.>

<Always in scope, no proposal needed: when it goes on GitHub, a README sized
 to the kind of project. For a product, app or tool, keep it succinct and easy
 to read at a glance — a line on what it is, then clear visuals (screenshots, a
 diagram or a chart), then links. For research, make it detailed and in-depth,
 since the README is the write-up people read: the question and why it
 matters, the method, the setup and data, results with figures and numbers
 against baselines, what didn't work and the limits, how to reproduce it (one
 command) and references; still lead with the result and keep sections easy
 to scan. Either way, setup and the rest go in linked files:
 docs/INSTRUCTIONS.md (setup, run, use),
 docs/SYSTEM-DESIGN.md (see below) and docs/FILE-STRUCTURE.md (what's where). If what you're
 building is an application rather than a script, also a small unobtrusive feedback tab, and a settings
 button or tab (⌘, on the Mac) that gathers its preferences in one place.>

<Always in scope: a system design doc in the codebase, docs/SYSTEM-DESIGN.md,
 kept current as the build changes. Cover the architecture (with a Mermaid
 diagram), each component's job, the main flows, where data lives, the key
 design decisions and their trade-offs, how it's tested, and known limits.>

<Always in scope: a prompt log, docs/PROMPTS.md, kept current in every
 session. Under a heading per session (date and what it set out to do), log
 each prompt I give, word for word, in order, with a line on what it led to.
 Redact secrets, keys and personal data, and link it from the README.>

<Keep the changelog at the bottom current.>

<Git rules (no Claude attribution, never commit .claude/) are in
 ~/.claude/CLAUDE.md and apply on their own — nothing to repeat here.>

<Finish by listing every deliverable: path, what it is, how to check it works.>

## About you

<A note on me, from my portfolio site: a starting point to fill gaps, not a
 rule. Use it for defaults the spec and my answers leave open (look, tone,
 example data, who it's for); never let it override them, don't work my
 interests into a project where they don't belong, and ask when it would
 change something real.
 - Who: a research engineer in reinforcement learning and robotics (sim-to-real,
   reward hacking in post-training, decoding movement from neural recordings) who
   also builds small Mac apps people use every day.
 - Values: high agency, ambition, deep curiosity, caring and courage. Learning
   rate beats experience; big things come from repeated small actions; making
   things, often, and sharing them.
 - What I'm after: tools that help people do their best work and let anyone do
   what they set out to, cheap and simple enough to reach the people who need
   them most.
 - Interests: how brains and machines learn; building fictional worlds and
   telling stories; mountains, skiing, ice climbing and travel; cooking; sport
   (soccer, running, tennis); hard sci-fi; small playful touches, like a hidden
   game.
 - Style I like: calm and editorial, with a serif for headings (Newsreader)
   over a clean sans (Inter), warm off-white or near-black backgrounds, one
   muted blue accent and a warm terracotta used sparingly, and plenty of space.
   Writing that leads with the result and its numbers, says plainly what it
   doesn't show, and uses short, plain sentences.>

<My taste profile: what I gravitate to, from how I've reacted to builds. Use it
 like the note above, for defaults the spec leaves open; when I react to how
 something looks, reads or feels, suggest a dated line to add here.
 - Colour: one muted accent, with colour only where it carries meaning. Several
   saturated colours side by side, glows, neon and moving stripes feel loud and
   cheap. Warm, calm palettes; dark mode that stays quiet.
 - Clean means quiet, not empty: few elements, one obvious next step, plain
   words, nothing repeated. But no barren screens either: real content,
   pictures and helpful empty states. Simple and intuitive over decorated.
 - Density: built for someone who knows what they're doing. Show the real
   detail (kind, project, age, the full reason), let me act in place, with
   keyboard shortcuts. Cut clutter, not information; never feel like it's
   talking down to me.
 - Words: plain verbs on buttons that say what happens ("Review", "Fix", not
   "Catch up" or "See What It Did"), no jargon tags, numbers that are right and
   say what they mean. A wrong or misleading number is worse than none.
 - Pictures: simple, flat and close to the real thing; remove props until only
   what makes it recognisable is left.
 - How I think: push back and make me think; show what a suggestion rests on and
   how to check it; teach the idea so I can do it myself next time; take the
   simplest thing that works; think several steps ahead.>

<Before any paid API call, settle who pays, a spending cap, test versus live mode and where keys live, and keep a mock mode so the build runs without spending.>

<When the look, concept or UI direction is open, show two or three concrete mockups or concepts to pick from before building. Never redesign existing UI without asking.>

<Ask early for real sample inputs and working credentials, and check against the live API, model or tool as soon as one path works. When none exist, say so rather than inventing them silently.>

<Before building, write down done criteria with concrete thresholds or formulas for every vague term, plus a list of what is explicitly deferred, and confirm both with me.>

<Before building anything that judges, scores or generates content, decide with me whether an AI model or deterministic rules produce it, weighing cost, explainability and reproducibility, and which model is the default.>

<Validate any generated or computed content against primary sources and cite them, and label every estimate, approximation or invented parameter as such, so nothing fabricated passes as fact.>

<Before publishing anything, confirm which personal details, documents and contact info go public, and get consent from anyone featured.>

<Add a short manual review checklist for what automated tests can't verify, such as hardware, live services, sound, feel or taste, and walk through it with me before calling the build done.>

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
- 2026-11-09 — updated the meta-instructions to the current meta doc
- 2026-11-19 — updated the meta-instructions to the current meta doc
