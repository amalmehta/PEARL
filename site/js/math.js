// Typesets every [data-tex] element with KaTeX. If the CDN script didn't load, the Unicode fallback text stays.
// An equation too wide for a phone can carry a data-tex-narrow version (e.g. split over two lines).
const narrow = window.matchMedia("(max-width: 560px)");

function render() {
  for (const el of document.querySelectorAll("[data-tex]")) {
    const displayMode = el.parentElement.classList.contains("eq");
    const tex = (narrow.matches && el.dataset.texNarrow) || el.dataset.tex;
    try { window.katex.render(tex, el, { displayMode, throwOnError: false }); } catch {}
  }
}

export function mountMath() {
  if (!window.katex) return;
  render();
  if (document.querySelector("[data-tex-narrow]")) narrow.addEventListener("change", render);
}
