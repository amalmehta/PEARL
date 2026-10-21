// Preferences in one place. Persisted per viewer in localStorage (best effort).
const DEFAULTS = { theme: "system", speed: 30, ghosts: true };
const listeners = [];

function read() {
  try { return { ...DEFAULTS, ...JSON.parse(localStorage.getItem("pearl-settings") || "{}") }; }
  catch { return { ...DEFAULTS }; }
}

export const settings = read();

export function onSettings(fn) { listeners.push(fn); }

function apply() {
  const t = settings.theme;
  if (t === "system") document.documentElement.removeAttribute("data-theme");
  else document.documentElement.setAttribute("data-theme", t);
  try { localStorage.setItem("pearl-settings", JSON.stringify(settings)); } catch { /* private mode */ }
  listeners.forEach((fn) => fn(settings));
}

export function mountSettings() {
  const dlg = document.getElementById("settings");
  const form = dlg.querySelector("form");
  const open = () => { form.theme.value = settings.theme; form.speed.value = settings.speed; form.ghosts.checked = settings.ghosts; dlg.showModal(); };
  document.querySelectorAll("[data-open-settings]").forEach((b) => b.addEventListener("click", open));
  window.addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === ",") { e.preventDefault(); open(); }
  });
  form.addEventListener("input", () => {
    settings.theme = form.theme.value;
    settings.speed = Number(form.speed.value);
    settings.ghosts = form.ghosts.checked;
    form.querySelector("output").textContent = `${settings.speed} steps/s`;
    apply();
  });
  dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
  apply();
}
