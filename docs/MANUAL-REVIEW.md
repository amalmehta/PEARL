# Manual Review Checklist

These are things the automated tests can't judge. Tick each one on the published site and on a local run.

## Feel and smoothness

- [ ] Clicking the canvas moves the goal (or the wind) immediately, with no visible delay (< 100 ms).
- [ ] The robot moves at a steady rate with no stutter, including while scrolling the page.
- [ ] Switching task family keeps the last frame visible (dimmed) until the new weights load. There's no blank box or jump.
- [ ] The belief bars and return bars ease into place (about 200 ms), with no flicker.
- [ ] Dragging the product-of-Gaussians sliders redraws on every input event without lag.
- [ ] Hovering the result charts shows the readout immediately. Moving out hides it smoothly.
- [ ] Nothing shifts layout as fonts, data or charts load (canvas and chart boxes have fixed aspect ratios).
- [ ] Profile: in DevTools Performance, record 10 s of the demo at speed 120. Every frame should stay under 16 ms of scripting; record the worst frame here: ____ ms.

## Look

- [ ] Light mode: warm, restrained, with accents used sparingly.
- [ ] Dark mode, via both the system setting and Settings → Dark: check every component (header, demo, sliders, charts, tables, dialog, feedback tab, code blocks).
- [ ] Phone width (375 px): no horizontal scroll, the demo stacks, the sliders stack, the header nav hides.
- [ ] The icon reads as "a pearl under a belief curve" in the browser tab at 16 px.

## Content

- [ ] Every number on the page matches `results/RESULTS.md`.
- [ ] Estimates, reported-not-reproduced claims, and invented parameters are labelled.
- [ ] The links to the paper, PMLR, oyster and the repo all resolve.

## Settings and feedback

- [ ] ⌘, opens Settings. Theme, speed and the ghost-lines toggle apply live and persist after a reload.
- [ ] The Feedback tab opens a pre-filled GitHub issue.

## Live service

- [ ] The GitHub Pages deploy succeeded and the site loads over HTTPS with no console errors.
