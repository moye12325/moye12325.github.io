// scripts/fix-trailing-slash.js
// Normalize internal links to trailing-slash form.
//
// The theme's sidebar statistics widget emits url_for(config.tag_dir) etc.,
// which produces "/tags" (no trailing slash). With Vercel trailingSlash:true
// every such link is a 308 redirect — Google rediscovered them on every crawl
// and kept 126 URLs in the "Page with redirect" report.
//
// This filter rewrites internal hrefs that have no file extension and no
// trailing slash (anchors/queries preserved), e.g. /tags -> /tags/.
"use strict";

hexo.extend.filter.register("after_render:html", function (str, data) {
  if (typeof str !== "string") return str;

  return str.replace(/href="(\/[^"#?]*?)(")/g, function (m, path, closeQuote) {
    if (path === "/" || path.endsWith("/") || /\.[a-z0-9]+$/i.test(path)) return m;
    return 'href="' + path + '/' + closeQuote;
  });
}, 25);
