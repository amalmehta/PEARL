// Typesets every [data-tex] element with KaTeX. If the CDN script didn't load, the Unicode fallback text stays.
export function mountMath() {
  if (!window.katex) return;
  for (const el of document.querySelectorAll("[data-tex]")) {
    const displayMode = el.parentElement.classList.contains("eq") || !!el.parentElement.closest(".eq-pair");
    try { window.katex.render(el.dataset.tex, el, { displayMode, throwOnError: false }); } catch {}
  }
}
