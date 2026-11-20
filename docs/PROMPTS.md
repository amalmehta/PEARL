# Prompt Log

Every prompt given to the coding agent, word for word, in order, with what it led to. Earlier sessions (2026-10-20, the original build) were not logged.

## 2026-11-19: find 10 more things to improve; README; publish to GitHub

1. > PEARL: update this existing project. It's already built, so change what's here rather than starting it again.
   >
   > What I want changed, in my words:
   > open this up and find 10 more things to improve about it.
   >
   > Bring it up to standard too, where it isn't already:
   > - Write a README: Write a short README: one line on what it is, a visual, and links to instructions.
   > - Publish it to GitHub: Create a GitHub repository for this project (following the naming rules in the spec, if any) and push it.
   >
   > How to go about it:
   > - Read PEARL.md and follow its META-INSTRUCTIONS, then the README and docs, and work the way the project already does.
   > - Edit what's here in place. Before rewriting a file wholesale or deleting anything, show me what would change and wait for my yes.
   > - Keep the README and docs in step with what changes, and add a CHANGELOG line if the project keeps one.

   Led to: the finding that the experiment suite had never finished. Ten improvements: checkpoint-resume, `make status`, "not run yet" states, demo weight provenance, the author order fixed, the training-loop pseudo-code corrected, an opening animation, draw-on-change in the demo, a browser-vs-PyTorch parity test, and docs corrected (suite time, wind range). Also a README, this log, a viz log, and the public GitHub repo.

2. Answers in the question widget: "Add resume, run full suite (Recommended)"; "Keep ±0.08, fix the spec (Recommended)".

   Led to: the full suite started in the background, and the spec's wind range changed to ±0.08.

3. > Yes, when it's done

   Led to: a background watcher that waited for the suite to finish, then this check-and-publish step.

4. > how's the suite going?

   Led to: a progress report (8 of 24 runs going, slowed by other load on the machine).

5. > Publish, labelled

   Given after the finished suite showed sparse Point-Robot missing its done criteria. Led to: results exported and published, with the shortfall stated in the README, the result sentences, the demo caption, Limits and SYSTEM-DESIGN.

6. > Train sparse longer

   Led to: finished runs can now be trained further by raising `num_iterations`. Sparse Point-Robot's budget went from 150 to 300 iterations, and its 3 seeds were resumed from iteration 150.

7. > look at the equation typeset. make it way more clean

   Led to: the display equations typeset like a paper (no cards, numbered, consistent notation), a two-line phone form for the widest one, and inline code that wraps on narrow screens.
