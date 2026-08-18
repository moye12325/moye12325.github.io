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
//      in the theme-bundled mermaid.min.js and renders the diagrams. The loader
//      is marked data-swup-reload-script so it is re-executed when the page is
//      swapped in via swup (single-page navigation).


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

// 2. Load mermaid only on pages that have diagrams, and only once per page.
hexo.extend.filter.register('after_post_render', function (data) {
  if (typeof data.content !== 'string' || !data.content.includes('class="mermaid"')) return;

  const loader = [
    '<script src="/js/build/libs/mermaid.min.js" data-swup-reload-script></script>',
    '<script data-swup-reload-script>',
    '(function () {',
    '  function renderMermaid() {',
    '    if (!window.mermaid) return;',
    '    try {',
    '      window.mermaid.initialize({ startOnLoad: false });',
    '      window.mermaid.run({ query: ".mermaid" });',
    '    } catch (e) {}',
    '  }',
    '  if (window.mermaid) {',
    '    renderMermaid();',
    '  } else {',
    '    var timer = setInterval(function () {',
    '      if (window.mermaid) { clearInterval(timer); renderMermaid(); }',
    '    }, 100);',
    '    setTimeout(function () { clearInterval(timer); renderMermaid(); }, 10000);',
    '  }',
    '  try {',
    '    if (window.swup) swup.hooks.on("page:view", renderMermaid);',
    '  } catch (e) {}',
    '})();',
    '</script>'
  ].join('\n');

  data.content += '\n' + loader;
}, 9);
