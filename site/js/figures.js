// Explainer figure (product of Gaussians) and results charts drawn from results/summary.json.
const NS = "http://www.w3.org/2000/svg";
const el = (tag, attrs = {}, parent) => {
  const e = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  if (parent) parent.appendChild(e);
  return e;
};
const pdf = (x, m, v) => Math.exp(-((x - m) ** 2) / (2 * v)) / Math.sqrt(2 * Math.PI * v);

// ---- Figure: each transition is a Gaussian vote; the posterior is their product -----------------
export function mountProduct(root) {
  const svg = root.querySelector("svg");
  const W = 640, H = 220, X0 = -4, X1 = 4;
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  const sx = (x) => ((x - X0) / (X1 - X0)) * W;
  const factors = [{ m: -1.2, s: 1.4 }, { m: 0.8, s: 1.0 }, { m: 1.6, s: 1.8 }];
  const sliders = root.querySelector(".sliders");
  const colors = ["--f1", "--f2", "--f3"];
  sliders.innerHTML = factors.map((f, i) => `
    <fieldset style="--c:var(${colors[i]})"><legend>Transition ${i + 1}</legend>
      <label>mean <input type="range" min="-3" max="3" step="0.05" value="${f.m}" data-i="${i}" data-k="m"></label>
      <label>width σ <input type="range" min="0.3" max="3" step="0.05" value="${f.s}" data-i="${i}" data-k="s"></label>
      <label class="check"><input type="checkbox" checked data-i="${i}" data-k="on"> included</label>
    </fieldset>`).join("");
  factors.forEach((f) => (f.on = true));
  const paths = factors.map((_, i) => el("path", { class: "factor", style: `stroke:var(${colors[i]})` }, svg));
  const prod = el("path", { class: "product" }, svg);
  el("line", { x1: 0, x2: W, y1: H - 20, y2: H - 20, class: "axis" }, svg);
  const readout = root.querySelector(".readout");

  function curve(m, v, scale) {
    let d = "";
    for (let px = 0; px <= W; px += 3) {
      const x = X0 + (px / W) * (X1 - X0);
      d += `${px ? "L" : "M"}${px},${(H - 20 - pdf(x, m, v) * scale).toFixed(1)}`;
    }
    return d;
  }
  function update() {
    let prec = 0, wm = 0;
    factors.forEach((f, i) => {
      paths[i].setAttribute("d", curve(f.m, f.s * f.s, 150));
      paths[i].style.opacity = f.on ? 1 : 0.15;
      if (f.on) { prec += 1 / (f.s * f.s); wm += f.m / (f.s * f.s); }
    });
    if (prec === 0) { prod.setAttribute("d", ""); readout.textContent = "No context: q(z|c) falls back to the prior N(0, 1)."; return; }
    const v = 1 / prec, m = wm * v;
    prod.setAttribute("d", curve(m, v, 150));
    readout.innerHTML = `posterior: mean <b>${m.toFixed(2)}</b>, σ <b>${Math.sqrt(v).toFixed(2)}</b>, which is narrower than every factor (σ<sub>min</sub> = ${Math.min(...factors.filter((f) => f.on).map((f) => f.s)).toFixed(2)})`;
  }
  sliders.addEventListener("input", (e) => {
    const { i, k } = e.target.dataset;
    factors[i][k] = k === "on" ? e.target.checked : Number(e.target.value);
    update();
  });
  update();
}

// ---- results charts --------------------------------------------------------------------------
const VARIANT = {
  pearl: ["PEARL", "--accent"], deterministic: ["Deterministic z", "--c-blue"],
  rnn_transitions: ["RNN, shuffled transitions", "--c-violet"], rnn_trajectories: ["RNN, whole trajectories", "--c-violet2"],
  ctx_offpolicy: ["Context from whole buffer", "--c-teal"], ctx_rlbatch: ["Context = RL batch", "--c-teal2"],
};

function chart(container, { series, xlabel, ylabel, refLines = [], xs }) {
  const W = 320, H = 210, L = 44, R = 10, T = 10, B = 34;
  const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, class: "chart", role: "img" });
  const all = series.flatMap((s) => s.ys.flat()).concat(refLines.map((r) => r.y));
  let lo = Math.min(...all), hi = Math.max(...all);
  const pad = (hi - lo) * 0.08 || 1; lo -= pad; hi += pad;
  const x0 = Math.min(...xs), x1 = Math.max(...xs);
  const sx = (x) => L + ((x - x0) / (x1 - x0 || 1)) * (W - L - R);
  const sy = (y) => T + (1 - (y - lo) / (hi - lo)) * (H - T - B);
  for (let i = 0; i <= 4; i++) {
    const y = lo + ((hi - lo) * i) / 4;
    el("line", { x1: L, x2: W - R, y1: sy(y), y2: sy(y), class: "grid" }, svg);
    el("text", { x: L - 6, y: sy(y) + 3, class: "tick", "text-anchor": "end" }, svg).textContent = y.toFixed(Math.abs(hi - lo) < 5 ? 1 : 0);
  }
  [x0, (x0 + x1) / 2, x1].forEach((x) => {
    el("text", { x: sx(x), y: H - B + 14, class: "tick", "text-anchor": "middle" }, svg).textContent = Number.isInteger(x) ? x : x.toFixed(0);
  });
  el("text", { x: (L + W - R) / 2, y: H - 4, class: "axis-label", "text-anchor": "middle" }, svg).textContent = xlabel;
  el("text", { x: 10, y: (T + H - B) / 2, class: "axis-label", "text-anchor": "middle", transform: `rotate(-90 10 ${(T + H - B) / 2})` }, svg).textContent = ylabel;
  for (const ref of refLines) {
    el("line", { x1: L, x2: W - R, y1: sy(ref.y), y2: sy(ref.y), class: "ref" }, svg);
    el("text", { x: W - R, y: sy(ref.y) - 4, class: "tick", "text-anchor": "end" }, svg).textContent = ref.label;
  }
  for (const s of series) {
    const n = s.ys.length;
    const mean = xs.map((_, j) => s.ys.reduce((a, y) => a + y[j], 0) / n);
    const sd = xs.map((_, j) => Math.sqrt(s.ys.reduce((a, y) => a + (y[j] - mean[j]) ** 2, 0) / n));
    const band = xs.map((x, j) => `${sx(x)},${sy(mean[j] + sd[j])}`).concat(xs.map((x, j) => `${sx(x)},${sy(mean[j] - sd[j])}`).reverse());
    el("polygon", { points: band.join(" "), style: `fill:var(${s.color});opacity:.15` }, svg);
    s.ys.forEach((y) => el("polyline", { points: xs.map((x, j) => `${sx(x)},${sy(y[j])}`).join(" "), class: "seed", style: `stroke:var(${s.color})` }, svg));
    el("polyline", { points: xs.map((x, j) => `${sx(x)},${sy(mean[j])}`).join(" "), class: "mean", style: `stroke:var(${s.color})` }, svg);
    s.mean = mean; s.sd = sd;
  }
  // hover readout
  const hover = el("line", { y1: T, y2: H - B, class: "hover" }, svg);
  const tip = document.createElement("div"); tip.className = "tip";
  svg.addEventListener("pointermove", (e) => {
    const r = svg.getBoundingClientRect();
    const px = ((e.clientX - r.left) / r.width) * W;
    let j = 0, best = Infinity;
    xs.forEach((x, k) => { const d = Math.abs(sx(x) - px); if (d < best) { best = d; j = k; } });
    hover.setAttribute("x1", sx(xs[j])); hover.setAttribute("x2", sx(xs[j])); hover.style.opacity = 1;
    tip.innerHTML = `<b>${xlabel}: ${xs[j]}</b>` + series.map((s) => `<div><i style="background:var(${s.color})"></i>${s.label}: ${s.mean[j].toFixed(2)} ± ${s.sd[j].toFixed(2)}</div>`).join("");
    tip.style.opacity = 1;
  });
  svg.addEventListener("pointerleave", () => { hover.style.opacity = 0; tip.style.opacity = 0; });
  const legend = document.createElement("div"); legend.className = "legend";
  legend.innerHTML = series.map((s) => `<span><i style="background:var(${s.color})"></i>${s.label} (n=${s.ys.length})</span>`).join("");
  container.append(svg, legend, tip);
}

const ENV_LABEL = { point: "Point-Robot (dense)", sparse_point: "Sparse Point-Robot", point_wind: "Point-Wind (invented)" };

export async function mountResults() {
  let summary;
  try { summary = await fetch("data/summary.json").then((r) => r.json()); }
  catch { return; }
  const runs = summary.runs;
  document.querySelectorAll("[data-chart]").forEach((box) => {
    const [kind, env, ...variants] = box.dataset.chart.split(":");
    const vs = variants.length ? variants : ["pearl"];
    const sel = vs.map((v) => runs[`${env}/${v}`]).filter(Boolean);
    if (!sel.length) return;
    const head = document.createElement("h4"); head.textContent = box.dataset.title || ENV_LABEL[env];
    box.append(head);
    if (kind === "learning") {
      chart(box, {
        xs: sel[0].env_steps.map((s) => Math.round(s / 1000)), xlabel: "env steps (k)", ylabel: "return, last trajectory",
        refLines: [{ y: summary.random_policy[env], label: "random actions" }, { y: summary.oracle[env], label: "oracle (knows the task)" }],
        series: sel.map((r) => ({ label: VARIANT[r.variant][0], color: VARIANT[r.variant][1], ys: r.final_return.map((y) => y.slice(0, sel[0].env_steps.length)) })),
      });
    } else {
      chart(box, {
        xs: sel[0].adaptation[0].map((_, i) => i + 1), xlabel: "trajectory in episode", ylabel: "return",
        refLines: [{ y: summary.oracle[env], label: "oracle" }],
        series: sel.map((r) => ({ label: VARIANT[r.variant][0], color: VARIANT[r.variant][1], ys: r.adaptation })),
      });
    }
  });
  document.querySelectorAll("[data-stat]").forEach((n) => {
    const [key, field] = n.dataset.stat.split("|");
    const r = runs[key];
    if (!r) return;
    n.textContent = field === "final" ? `${r.final_mean.toFixed(2)} ± ${r.final_std.toFixed(2)}`
      : field === "first" ? r.first_traj_mean.toFixed(2) : field === "random" ? summary.random_policy[r.env].toFixed(2) : "";
  });
}
