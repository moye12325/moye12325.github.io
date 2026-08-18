// scripts/clean-public.js
// Post-build cleanup of the generated site (run automatically by `npm run build`).
// Removes files that are deployed but never referenced by any page:
//   - source maps (*.map)
//   - public/js/libs/ (the theme's raw source copy; only js/build/ is used)
//   - FontAwesome weights that are disabled in _config.redefine.yml
//     (thin/light/duotone/sharp) and their unneeded CSS bundles
"use strict";

const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const publicDir = path.join(root, "public");

if (!fs.existsSync(publicDir)) {
  console.log("[clean-public] no public dir, skip");
  process.exit(0);
}

let removedFiles = 0;
let removedBytes = 0;

function remove(file) {
  const abs = path.resolve(file);
  if (!abs.startsWith(publicDir + path.sep)) {
    console.error("[clean-public] refuse to remove outside public:", abs);
    process.exit(1);
  }
  if (!fs.existsSync(abs)) return;
  const st = fs.statSync(abs);
  if (st.isDirectory()) {
    fs.rmSync(abs, { recursive: true, force: true });
  } else {
    removedBytes += st.size;
    fs.rmSync(abs, { force: true });
  }
  removedFiles++;
  console.log("[clean-public] removed", path.relative(publicDir, abs));
}

// 1. source maps
function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(full);
    } else if (entry.name.endsWith(".map")) {
      remove(full);
    }
  }
}
walk(publicDir);

// 2. theme raw js copy (not referenced; mermaid etc. are under js/build/)
remove(path.join(publicDir, "js", "libs"));

// 3. disabled FontAwesome weights
for (const name of ["fa-thin-100", "fa-light-300", "fa-duotone-900", "fa-sharp-solid-900"]) {
  for (const ext of [".ttf", ".woff2", ".woff"]) {
    remove(path.join(publicDir, "webfonts", name + ext));
  }
}

// 4. unneeded FontAwesome css bundles
for (const name of ["all.min.css", "duotone.min.css", "thin.min.css", "light.min.css"]) {
  remove(path.join(publicDir, "fontawesome", name));
}

console.log(`[clean-public] done: ${removedFiles} files, freed ${(removedBytes / 1024 / 1024).toFixed(1)} MB`);
