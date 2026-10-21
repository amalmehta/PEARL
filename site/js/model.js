// The trained PEARL agent and its environments, in plain JS (mirrors pearl/agent.py and pearl/envs.py).
// Weights come from `python -m pearl.export` as base64 little-endian float32.

function f32(b64) {
  const bin = atob(b64);
  const u = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i);
  return new Float32Array(u.buffer);
}

function layer(L) {
  return { W: f32(L.w), b: f32(L.b), out: L.shape[0], inp: L.shape[1] };
}

function linear(L, x) {
  const y = new Float32Array(L.out);
  for (let o = 0; o < L.out; o++) {
    let s = L.b[o];
    const off = o * L.inp;
    for (let i = 0; i < L.inp; i++) s += L.W[off + i] * x[i];
    y[o] = s;
  }
  return y;
}

const relu = (x) => x.map((v) => (v > 0 ? v : 0));
const softplus = (v) => (v > 20 ? v : Math.log1p(Math.exp(v)));

export function gaussian(rng) {
  // Box–Muller
  let u = 0;
  while (u === 0) u = rng();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * rng());
}

export function mulberry32(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export class Agent {
  constructor(data) {
    this.d = data.latent;
    this.policyHidden = data.policy.hidden.map(layer);
    this.policyMean = layer(data.policy.mean);
    this.encHidden = data.encoder.hidden.map(layer);
    this.encOut = layer(data.encoder.out);
  }

  // deterministic action = tanh(mean), as in evaluation
  act(obs, z) {
    let h = Float32Array.from([...obs, ...z]);
    for (const L of this.policyHidden) h = relu(linear(L, h));
    return Array.from(linear(this.policyMean, h), Math.tanh);
  }

  // one transition -> one Gaussian factor Psi(z | c_n)
  factor(feat) {
    let h = Float32Array.from(feat);
    for (const L of this.encHidden) h = relu(linear(L, h));
    const p = linear(this.encOut, h);
    const mu = Array.from(p.slice(0, this.d));
    const v = Array.from(p.slice(this.d), (x) => Math.max(softplus(x), 1e-7));
    return { mu, v };
  }
}

// Running product of Gaussians: precisions add, means are precision-weighted.
export class Posterior {
  constructor(d) { this.d = d; this.reset(); }
  reset() { this.prec = new Array(this.d).fill(0); this.wmu = new Array(this.d).fill(0); this.n = 0; }
  add({ mu, v }) {
    for (let i = 0; i < this.d; i++) { this.prec[i] += 1 / v[i]; this.wmu[i] += mu[i] / v[i]; }
    this.n++;
  }
  get() {
    if (this.n === 0) return prior(this.d);
    const v = this.prec.map((p) => 1 / p);
    return { mu: this.wmu.map((w, i) => w * v[i]), v };
  }
}

export const prior = (d) => ({ mu: new Array(d).fill(0), v: new Array(d).fill(1) });

export function sampleZ(belief, rng) {
  return belief.mu.map((m, i) => m + Math.sqrt(belief.v[i]) * gaussian(rng));
}

const clip = (a) => Math.max(-1, Math.min(1, a));

export class Env {
  constructor(data, rng) { this.cfg = data; this.rng = rng; }
  setTask(task) { this.task = task; }
  get goal() { return this.cfg.env === "point_wind" ? [0, 0] : this.task; }
  get wind() { return this.cfg.env === "point_wind" ? this.task : [0, 0]; }
  reset() {
    this.s = this.cfg.env === "sparse_point" ? [0, 0] : [this.rng() * 2 - 1, this.rng() * 2 - 1];
    return this.s.slice();
  }
  stepFrom(s, a) {
    const w = this.wind;
    return [s[0] + 0.1 * clip(a[0]) + w[0], s[1] + 0.1 * clip(a[1]) + w[1]];
  }
  reward(s) {
    const g = this.goal;
    const dense = -Math.hypot(s[0] - g[0], s[1] - g[1]);
    if (!this.cfg.sparse) return dense;
    return dense >= -this.cfg.goal_radius ? 1 + dense : 0;
  }
  step(a) {
    const s0 = this.s;
    this.s = this.stepFrom(s0, a);
    const r = this.reward(this.s);
    const feat = [...s0, ...a, r, ...(this.cfg.use_next_obs ? this.s : [])];
    return { s: this.s.slice(), r, feat };
  }
}
