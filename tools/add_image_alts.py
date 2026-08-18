# -*- coding: utf-8 -*-
"""Add alt text to images that lack it in posts.

- Skips images that already have an alt.
- Skips fenced code blocks.
- Only writes a file when at least one image actually got an alt.
- Alt format: "<title> 配图 N" (title truncated to keep it short).
Reusable: python tools/add_image_alts.py
"""
import io
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

POSTS_ROOT = os.path.join(os.path.dirname(__file__), "..", "source", "_posts")
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^\s*```")


def front_title(lines):
    if not lines or lines[0].strip() != "---":
        return None
    for ln in lines[1:]:
        if ln.strip() == "---":
            break
        m = re.match(r"^title:\s*(.*)$", ln)
        if m:
            return m.group(1).strip().strip("\"'")
    return None


def process(path):
    with io.open(path, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(nl)

    title = front_title(lines) or os.path.splitext(os.path.basename(path))[0]
    title = re.sub(r"[\s:：/\\|*]+", " ", title).strip()
    if len(title) > 18:
        title = title[:18].rstrip()

    in_code = False
    count = 0
    replaced = False
    for i, ln in enumerate(lines):
        if FENCE_RE.match(ln):
            in_code = not in_code
            continue
        if in_code:
            continue

        def repl(m):
            nonlocal count, replaced
            alt, url = m.group(1), m.group(2)
            if alt:
                return m.group(0)
            count += 1
            replaced = True
            return "![%s 配图 %d](%s)" % (title, count, url)

        lines[i] = IMG_RE.sub(repl, ln)

    if not replaced:
        return False
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(nl.join(lines) + nl)
    return True


def main():
    changed = total_img = 0
    for root, _dirs, files in os.walk(POSTS_ROOT):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            with io.open(p, "r", encoding="utf-8", newline="") as f:
                before = f.read()
            total_img += len(IMG_RE.findall(before))
            if process(p):
                changed += 1
    print(f"files with images alted={changed} total images seen={total_img}")


if __name__ == "__main__":
    main()
