// Result sentences are generated from data/summary.json, so the prose can never drift from the numbers.
const fmt = (r) => `${r.final_mean.toFixed(2)} ± ${r.final_std.toFixed(2)}`;

export async function mountText() {
  let s;
  try { s = await fetch("data/summary.json").then((r) => r.json()); } catch { return; }
  const R = s.runs, rand = s.random_policy;
  const envs = [["point", "Dense Point-Robot"], ["sparse_point", "Sparse Point-Robot"], ["point_wind", "Point-Wind"]];

  const learn = envs.filter(([e]) => R[`${e}/pearl`]).map(([e, name]) => {
    const r = R[`${e}/pearl`];
    return `<b>${name}</b>: the last trajectory scores ${fmt(r)}, against ${rand[e].toFixed(2)} for random actions and ${s.oracle[e].toFixed(2)} for an oracle that knows the task`;
  });
  document.getElementById("results-text").innerHTML =
    `Return of the last trajectory of a meta-test episode on the 20 held-out tasks, after training (mean ± std over seeds). ${learn.join("; ")}.`;

  const adapt = envs.filter(([e]) => R[`${e}/pearl`]).map(([e, name]) => {
    const r = R[`${e}/pearl`];
    return `${name} goes from ${r.first_traj_mean.toFixed(2)} on the first trajectory (prior sample) to ${r.final_mean.toFixed(2)} on the last`;
  });
  document.getElementById("adapt-text").innerHTML =
    `The first trajectory acts on a prior sample. Later ones act on posterior samples. ${adapt.join("; ")}.`;

  const ab = [["deterministic", "deterministic z"], ["rnn_transitions", "RNN on shuffled transitions"],
    ["rnn_trajectories", "RNN on whole trajectories"], ["ctx_offpolicy", "context from the whole buffer"],
    ["ctx_rlbatch", "context = RL batch"]].filter(([v]) => R[`point/${v}`]);
  if (R["point/pearl"] && ab.length) {
    document.getElementById("ablation-text").innerHTML =
      `Final return on dense Point-Robot: PEARL ${fmt(R["point/pearl"])}; ` +
      ab.map(([v, name]) => `${name} ${fmt(R[`point/${v}`])}`).join("; ") +
      `. With 3 seeds, differences smaller than about one standard deviation are not meaningful.`;
  }
}
