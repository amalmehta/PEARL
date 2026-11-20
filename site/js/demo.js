// Interactive meta-test episode: explore with z ~ prior, then posterior sampling (pearl/trainer.py evaluate).
import { Agent, Env, Posterior, mulberry32, prior, sampleZ } from "./model.js";
import { settings, onSettings } from "./settings.js";

const ENV_INFO = {
  point: { label: "Point-Robot", hint: "Click anywhere to move the goal. Reward = minus the distance to it." },
  sparse_point: { label: "Sparse Point-Robot", hint: "Click to move the goal along the half circle. Reward only inside the ring." },
  point_wind: { label: "Point-Wind", hint: "Click to set the wind (arrow). The goal is fixed at the centre. An invented task family." },
};
const VIEW = 1.35; // world half-width shown

export async function mountDemo(root) {
  const $ = (s) => root.querySelector(s);
  const canvas = $("canvas");
  const ctx = canvas.getContext("2d");
  const cache = {};
  let data, agent, env, post, rng = mulberry32(7);
  let ep = null; // current episode state
  let playing = true, envName = "sparse_point", lastT = 0, acc = 0, pauseUntil = 0;
  // redraw only when something changed and the canvas is on screen (saves battery while reading)
  let dirty = true, visible = true;

  function css(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }

  function resize() {
    const dpr = window.devicePixelRatio || 1;
    const w = canvas.clientWidth;
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(w * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    dirty = true;
  }
  const W = () => canvas.clientWidth;
  const toPx = ([x, y]) => [(x / VIEW + 1) * W() / 2, (1 - y / VIEW) * W() / 2];
  const toWorld = (px, py) => [(px / W() * 2 - 1) * VIEW, (1 - py / W() * 2) * VIEW];

  async function load(name) {
    // show the last frame until the new weights arrive, never an empty box
    root.classList.add("loading");
    if (!cache[name]) cache[name] = fetch(`data/${name}.json`).then((r) => r.json());
    data = await cache[name];
    if (name !== envName) return; // a newer choice won
    agent = new Agent(data);
    env = new Env(data, rng);
    post = new Posterior(data.latent);
    root.classList.remove("loading");
    $(".hint").textContent = ENV_INFO[name].hint;
    const t = data.trained;
    $(".provenance").textContent = t
      ? `These weights: ${t.run}, trained ${t.iterations} of ${t.of_iterations} iterations (${Math.round(t.env_steps / 1000)}k env steps)` +
        (t.eval_final != null ? `; last-trajectory return on held-out tasks ${t.eval_final.toFixed(2)}.` : ".")
      : "These weights were exported before training details were recorded, from a partly trained run. Expect rough behaviour until they are re-exported from the finished suite.";
    newEpisode(data.eval_tasks[Math.floor(rng() * data.eval_tasks.length)]);
  }

  function newEpisode(task) {
    env.setTask(task);
    post.reset();
    ep = { trajs: [], returns: [], k: 0, belief: prior(data.latent), phase: "explore" };
    startTraj();
  }

  function startTraj() {
    const s = env.reset();
    ep.z = sampleZ(ep.belief, rng);
    ep.cur = { pts: [s], ret: 0, t: 0 };
    ep.ghosts = settings.ghosts ? imagine(s, 6) : [];
    renderPanel();
  }

  // where would the policy go under other samples from the current belief? (real dynamics)
  function imagine(s0, n) {
    const out = [];
    for (let i = 0; i < n; i++) {
      const z = sampleZ(ep.belief, rng);
      let s = s0; const pts = [s];
      for (let t = 0; t < data.horizon; t++) { s = env.stepFrom(s, agent.act(s, z)); pts.push(s); }
      out.push(pts);
    }
    return out;
  }

  function stepOnce() {
    const s = ep.cur.pts[ep.cur.pts.length - 1];
    const { s: s2, r, feat } = env.step(agent.act(s, ep.z));
    ep.cur.pts.push(s2); ep.cur.ret += r; ep.cur.t++; dirty = true;
    post.add(agent.factor(feat)); // context accumulates every step; it is *used* per trajectory
    if (ep.cur.t >= data.horizon) endTraj();
  }

  function endTraj() {
    ep.trajs.push(ep.cur.pts); ep.returns.push(ep.cur.ret); ep.k++;
    if (ep.k >= data.num_exp_traj_eval) { ep.belief = post.get(); ep.phase = "posterior"; }
    if (ep.k >= data.n_traj) { pauseUntil = performance.now() + 1600; ep.done = true; renderPanel(); return; }
    pauseUntil = performance.now() + 260;
    startTraj();
  }

  function frame(t) {
    const dt = Math.min(100, t - lastT); lastT = t;
    if (data && ep && playing && visible && t > pauseUntil) {
      if (ep.done) newEpisode(env.task);
      else {
        acc += dt * settings.speed / 1000;
        while (acc >= 1 && !ep.done && t > pauseUntil) { stepOnce(); acc -= 1; }
      }
    }
    if (data && ep && dirty && visible) { draw(); dirty = false; }
    requestAnimationFrame(frame);
  }

  function line(pts, color, width, alpha) {
    ctx.globalAlpha = alpha; ctx.strokeStyle = color; ctx.lineWidth = width;
    ctx.beginPath();
    pts.forEach((p, i) => { const [x, y] = toPx(p); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); });
    ctx.stroke(); ctx.globalAlpha = 1;
  }

  function draw() {
    const w = W(), ink = css("--ink"), muted = css("--muted"), accent = css("--accent"), line2 = css("--line");
    ctx.clearRect(0, 0, w, w);
    // grid + task distribution
    ctx.strokeStyle = line2; ctx.lineWidth = 1;
    for (let g = -1; g <= 1; g += 0.5) {
      const [x] = toPx([g, 0]); const [, y] = toPx([0, g]);
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, w); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
    }
    ctx.setLineDash([3, 5]); ctx.strokeStyle = muted; ctx.globalAlpha = 0.6;
    if (data.env === "sparse_point") {
      const [cx, cy] = toPx([0, 0]); ctx.beginPath(); ctx.arc(cx, cy, w / 2 / VIEW, Math.PI, 2 * Math.PI); ctx.stroke();
    } else if (data.env === "point") {
      const [x0, y0] = toPx([-1, 1]); ctx.strokeRect(x0, y0, w / VIEW, w / VIEW);
    }
    ctx.setLineDash([]); ctx.globalAlpha = 1;
    // goal
    const [gx, gy] = toPx(env.goal);
    const R = (data.sparse ? data.goal_radius : 0.06) * w / 2 / VIEW;
    ctx.fillStyle = accent; ctx.globalAlpha = 0.12; ctx.beginPath(); ctx.arc(gx, gy, R, 0, 7); ctx.fill();
    ctx.globalAlpha = 1; ctx.strokeStyle = accent; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(gx, gy, R, 0, 7); ctx.stroke();
    if (data.env === "point_wind") arrow([0, 0], [env.wind[0] * 10, env.wind[1] * 10], css("--accent2"));
    // ghosts: other hypotheses from the current belief
    for (const g of ep.ghosts) line(g, muted, 1, 0.35);
    // past trajectories fade with age
    ep.trajs.forEach((p, i) => line(p, i < data.num_exp_traj_eval ? css("--explore") : accent, 1.6,
      0.25 + 0.5 * (i + 1) / ep.trajs.length));
    line(ep.cur.pts, ep.phase === "explore" ? css("--explore") : accent, 2.6, 1);
    const [ax, ay] = toPx(ep.cur.pts[ep.cur.pts.length - 1]);
    ctx.fillStyle = ink; ctx.beginPath(); ctx.arc(ax, ay, 4.5, 0, 7); ctx.fill();
  }

  function arrow(from, vec, color) {
    const [x0, y0] = toPx(from); const [x1, y1] = toPx([from[0] + vec[0], from[1] + vec[1]]);
    ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 2.5;
    ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke();
    const a = Math.atan2(y1 - y0, x1 - x0);
    ctx.beginPath(); ctx.moveTo(x1, y1);
    ctx.lineTo(x1 - 9 * Math.cos(a - 0.5), y1 - 9 * Math.sin(a - 0.5));
    ctx.lineTo(x1 - 9 * Math.cos(a + 0.5), y1 - 9 * Math.sin(a + 0.5)); ctx.fill();
  }

  // side panel: belief width per latent dim and return per trajectory (CSS transitions do the easing)
  function renderPanel() {
    dirty = true;
    const sd = ep.belief.v.map(Math.sqrt);
    $(".bars").innerHTML = sd.map((s, i) =>
      `<div class="bar"><span>z${i + 1}</span><i style="transform:scaleX(${Math.min(1, s).toFixed(3)})"></i><b>${s.toFixed(2)}</b></div>`).join("");
    const n = data.n_traj, rets = ep.returns;
    const lo = data.sparse ? 0 : Math.min(-20, ...rets), hi = data.sparse ? Math.max(5, ...rets) : 0;
    $(".returns").innerHTML = Array.from({ length: n }, (_, i) => {
      const r = rets[i];
      const h = r === undefined ? 0 : Math.max(0.03, (r - lo) / (hi - lo || 1));
      const cls = i < data.num_exp_traj_eval ? "explore" : "post";
      return `<i class="${cls}${r === undefined ? " empty" : ""}" style="--h:${h.toFixed(3)}" title="trajectory ${i + 1}: ${r === undefined ? "–" : r.toFixed(2)}"></i>`;
    }).join("");
    const k = Math.min(ep.k + 1, n);
    $(".status").textContent = ep.done ? "Episode done: a new one starts in a moment."
      : ep.phase === "explore" ? `Trajectory ${k}/${n}: exploring with z drawn from the prior`
      : `Trajectory ${k}/${n}: z drawn from the posterior after ${post.n} transitions`;
  }

  // ---- controls --------------------------------------------------------------------------
  canvas.addEventListener("pointerdown", (e) => {
    if (!data) return;
    const r = canvas.getBoundingClientRect();
    let [x, y] = toWorld(e.clientX - r.left, e.clientY - r.top);
    let task;
    if (data.env === "sparse_point") { const a = Math.atan2(Math.max(0, y), x); task = [Math.cos(a), Math.sin(a)]; }
    else if (data.env === "point_wind") task = [x, y].map((v) => Math.max(-0.08, Math.min(0.08, v / 10)));
    else task = [x, y].map((v) => Math.max(-1, Math.min(1, v)));
    pauseUntil = 0; newEpisode(task);
  });
  root.querySelectorAll("[data-env]").forEach((b) => b.addEventListener("click", () => {
    envName = b.dataset.env;
    root.querySelectorAll("[data-env]").forEach((x) => x.setAttribute("aria-pressed", x === b));
    load(envName);
  }));
  $(".play").addEventListener("click", (e) => { playing = !playing; e.currentTarget.textContent = playing ? "Pause" : "Play"; });
  $(".again").addEventListener("click", () => { pauseUntil = 0; newEpisode(data.eval_tasks[Math.floor(rng() * data.eval_tasks.length)]); });
  new ResizeObserver(resize).observe(canvas);
  onSettings(() => { if (ep) { ep.ghosts = settings.ghosts ? imagine(ep.cur.pts[0], 6) : []; } dirty = true; });
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => { dirty = true; });
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; dirty = true; }).observe(canvas);

  resize();
  await load(envName);
  requestAnimationFrame((t) => { lastT = t; frame(t); });
}
