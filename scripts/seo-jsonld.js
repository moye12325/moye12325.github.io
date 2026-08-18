// scripts/seo-jsonld.js
// Inject JSON-LD structured data before </head>:
//   - WebSite on every page
//   - BlogPosting + BreadcrumbList on post pages
//
// Note: registered under "after_render:html", which Hexo 8 stores/executes as
// "_after_html_render". The filter's second argument is the render locals;
// the post data itself lives at data.page, and data.path is the output path.
"use strict";

hexo.extend.filter.register("after_render:html", function (str, data) {
  if (typeof str !== "string" || !str.includes("</head>")) return str;

  const ctx = this;
  const page = (data && data.page) || {};
  const outPath = String((data && data.path) || page.path || "");
  const isPost = /^\d{4}\/\d{2}\/\d{2}\//.test(outPath);

  const siteName = (ctx.theme.info && ctx.theme.info.title) || ctx.config.title || "Blog";
  const siteUrl = String(ctx.config.url).replace(/\/+$/, "");
  const author = ctx.config.author || (ctx.theme.info && ctx.theme.info.author) || "";

  function absUrl(p) {
    if (!p) return null;
    if (/^https?:\/\//i.test(p)) return p;
    return siteUrl + (p.startsWith("/") ? p : "/" + p);
  }

  const schemas = [];

  schemas.push({
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: siteName,
    url: siteUrl + "/",
  });

  if (isPost) {
    const title = page.title || "";
    const description = page.description || page.summary || "";
    let canonical = (data && data.url) || siteUrl + "/" + outPath.replace(/^\/+/, "");
    canonical = canonical.replace(/index\.html$/, "");

    const datePub = page.date && page.date.toISOString ? page.date.toISOString() : null;
    const dateMod = page.updated && page.updated.toISOString ? page.updated.toISOString() : datePub;

    let image = page.og_image || null;
    if (!image && typeof page.content === "string") {
      const m = page.content.match(/<img[^>]+src=["']([^"']+)/i);
      if (m) image = m[1];
    }
    if (!image && ctx.theme.config && ctx.theme.config.global && ctx.theme.config.global.open_graph && ctx.theme.config.global.open_graph.image) {
      image = ctx.theme.config.global.open_graph.image;
    }
    image = absUrl(image);

    const keywords = [];
    if (page.tags && typeof page.tags.forEach === "function") {
      page.tags.forEach(function (t) {
        if (t == null) return;
        keywords.push(typeof t === "string" ? t : t.name || String(t));
      });
    }

    const blogPosting = {
      "@context": "https://schema.org",
      "@type": "BlogPosting",
      headline: title,
      description: description,
      mainEntityOfPage: { "@type": "WebPage", "@id": canonical },
      author: { "@type": "Person", name: author },
      publisher: { "@type": "Organization", name: siteName, url: siteUrl + "/" },
      datePublished: datePub,
      dateModified: dateMod,
    };
    if (image) blogPosting.image = image;
    if (keywords.length) blogPosting.keywords = keywords.join(", ");
    schemas.push(blogPosting);

    const crumbs = [{ name: "首页", item: siteUrl + "/" }];
    const firstCat =
      typeof page.categories === "string" ? page.categories
      : Array.isArray(page.categories) && page.categories.length
        ? (typeof page.categories[0] === "string" ? page.categories[0] : (page.categories[0] && page.categories[0].name) || null)
        : null;
    if (firstCat) {
      crumbs.push({ name: firstCat, item: siteUrl + "/categories/" + encodeURIComponent(firstCat) + "/" });
    }
    crumbs.push({ name: title, item: canonical });
    schemas.push({
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      itemListElement: crumbs.map((c, i) => ({
        "@type": "ListItem",
        position: i + 1,
        name: c.name,
        item: c.item,
      })),
    });
  }

  const json = JSON.stringify(schemas).replace(/</g, "\\u003c");
  return str.replace("</head>", '<script type="application/ld+json">' + json + "</script></head>");
}, 20);
