// Result sentences are generated from data/summary.json (passed in by mountResults, fetched once), so the prose can never drift from the numbers.
const fmt = (r) => `${r.final_mean.toFixed(2)} ± ${r.final_std.toFixed(2)}`;

export function mountText(s) {
  if (!s) {
    document.getElementById("results-text").textContent =
      "No results yet: the experiment suite is still running. The charts above, and the sentences that describe them, are generated from its output, so nothing here is typed in by hand.";
    return;
  }
  const R = s.runs, rand = s.random_policy;
  const envs = [["point", "Dense Point-Robot"], ["sparse_point", "Sparse Point-Robot"], ["point_wind", "Point-Wind"]];

  const learn = envs.filter(([e]) => R[`${e}/pearl`]).map(([e, name]) => {
    const r = R[`${e}/pearl`];
    // the spec's "Learns" done criterion: the mean ends closer to the oracle than to random actions
    const learns = Math.abs(r.final_mean - s.oracle[e]) < Math.abs(r.final_mean - rand[e]);
    return `<b>${name}</b>: the last trajectory scores ${fmt(r)}, against ${rand[e].toFixed(2)} for random actions and ${s.oracle[e].toFixed(2)} for an oracle that knows the task. ` +
      (learns ? "That is closer to the oracle than to random, so it passes the “learns” check"
              : "<b>That is closer to random than to the oracle, so it fails the “learns” check</b>");
  });
  document.getElementById("results-text").innerHTML =
    `Return of the last trajectory of a meta-test episode on the 20 held-out tasks, after training (mean ± std over seeds). ${learn.join(". ")}.`;

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
