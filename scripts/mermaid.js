// scripts/mermaid.js
// Render ```mermaid fenced blocks in posts.
//
// Why a custom script instead of the official hexo-filter-mermaid-diagrams?
//   - That plugin's regex only matches LF newlines, but this blog's posts are
//     CRLF, so the plugin silently did nothing.
//   - The theme's global mermaid toggle loads a ~2.5 MB mermaid.min.js on every
//     page. This script instead loads it only on pages that actually contain a
//     diagram, which keeps the rest of the site light.
//
// How it works:
//   1. before_post_render: convert ```mermaid fences to <pre class="mermaid">.
//   2. after_post_render: when a post has diagrams, append a loader that pulls
//      in the theme-bundled mermaid.min.js, renders the diagrams and applies
//      the light/dark theme + card styles. The loader is marked
//      data-swup-reload-script so it is re-executed when the page is swapped
//      in via swup (single-page navigation).
//
// Notes on the rendering logic:
//   - The mermaid.run() option key is querySelector (mermaid 11.x); `query`
//     throws "Nodes and querySelector are both undefined".
//   - The first render is deferred until after DOMContentLoaded. The theme's
//     scripts are loaded as type="module" and run BEFORE DOMContentLoaded, and
//     the theme saves each diagram's original source into data-original-code
//     at init (needed by its light/dark toggle). Rendering earlier would let
//     the theme capture the rendered SVG instead of the source, breaking the
//     toggle.


const MERMAID_REG = /(\s*)(`{3}) *(mermaid) *\r?\n?([\s\S]+?)\s*(\2)(\r?\n+|$)/g;

// 1. Convert fenced mermaid blocks into <pre class="mermaid"> elements.
hexo.extend.filter.register('before_post_render', function (data) {
  if (typeof data.content !== 'string' || !data.content.includes('```mermaid')) return;
  data.content = data.content.replace(
    MERMAID_REG,
    function (raw, start, open, lang, content, close, end) {
      return `${start}<pre class="mermaid">${content}</pre>${end}`;
    }
  );
}, 9);

// 2. Load mermaid only on pages that have diagrams, then render and style them.
hexo.extend.filter.register('after_post_render', function (data) {
  if (typeof data.content !== 'string' || !data.content.includes('class="mermaid"')) return;

  const loader = `<script src="/js/build/libs/mermaid.min.js" data-swup-reload-script></script>
<style data-swup-reload-script>
pre.mermaid {
  margin: 1.75rem auto !important;
  padding: 1.25rem 0.75rem !important;
  border: 1px solid var(--shadow-color-1) !important;
  border-radius: 10px !important;
  background-color: var(--background-color) !important;
  box-shadow: var(--redefine-box-shadow-flat) !important;
  text-align: center !important;
  overflow-x: auto !important;
}
pre.mermaid svg {
  max-width: 100% !important;
  height: auto !important;
}
</style>
<script data-swup-reload-script>
(function () {
  // Only set up once per page session; on swup navigation the loader scripts
  // of the incoming page are re-executed, and this guard prevents duplicate
  // swup handlers from accumulating.
  if (window.__mermaidLoader) return;
  window.__mermaidLoader = true;

  var LIGHT_THEME = "neutral";
  var DARK_THEME = "dark";

  function isDarkMode() {
    return document.documentElement.classList.contains("dark") ||
           document.body.classList.contains("dark-mode");
  }

  function renderMermaid() {
    if (!window.mermaid) return;
    var els = document.querySelectorAll(".mermaid");
    if (!els.length) return;

    // Keep the original diagram source so the theme's light/dark toggle can
    // restore and re-render it (its saveOriginalData() expects this attribute).
    Array.prototype.forEach.call(els, function (el) {
      if (!el.getAttribute("data-original-code")) {
        el.setAttribute("data-original-code", el.innerHTML);
      }
    });

    try {
      window.mermaid.initialize({
        startOnLoad: false, // we call run() ourselves; avoids double render
        theme: isDarkMode() ? DARK_THEME : LIGHT_THEME,
        fontFamily: '"PingFang SC", "Microsoft YaHei", "Helvetica Neue", Arial, "Noto Sans SC", sans-serif',
        flowchart: { curve: "basis", useMaxWidth: true, htmlLabels: true }
      });
      // NOTE: the option key is querySelector (mermaid 11.x); query throws.
      window.mermaid.run({ querySelector: ".mermaid" });
    } catch (e) {}
  }

  function renderWhenReady() {
    if (document.readyState === "loading") {
      // Wait for DOMContentLoaded: the theme (type="module", runs before
      // DOMContentLoaded) saves data-original-code first, so the toggle works.
      document.addEventListener("DOMContentLoaded", renderMermaid);
    } else {
      renderMermaid();
    }
  }

  if (window.mermaid) {
    renderWhenReady();
  } else {
    var timer = setInterval(function () {
      if (window.mermaid) { clearInterval(timer); renderWhenReady(); }
    }, 50);
    setTimeout(function () { clearInterval(timer); renderWhenReady(); }, 10000);
  }

  try {
    if (window.swup) swup.hooks.on("page:view", renderWhenReady);
  } catch (e) {}
})();
</script>`;

  data.content += '\n' + loader;
}, 9);
