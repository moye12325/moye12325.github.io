# -*- coding: utf-8 -*-
"""Backfill / fix `description` front matter for posts.

- Uses the existing `summary` when present (cleaned), otherwise extracts the
  first meaningful paragraph from the body.
- Skips posts that already have a sane `description`; regenerates ones that
  carry the `> ` folded-scalar artifact.
- Robust against mixed LF/CRLF newlines; writes back with the dominant style.
- Reusable: run `python scripts/add_post_descriptions.py`.
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
MAX_LEN = 120


def strip_md(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def truncate(text: str, limit: int = MAX_LEN) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    for ender in "。！？!?;；":
        idx = cut.rfind(ender)
        if idx >= limit * 0.5:
            return cut[: idx + 1]
    for sep in "，、 ,":
        idx = cut.rfind(sep)
        if idx >= limit * 0.5:
            return cut[:idx]
    return cut


def first_paragraph(body_lines, title: str):
    primary: list[str] = []
    fallback: list[str] = []
    in_code = False
    for raw in body_lines:
        s = raw.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not s:
            if primary or fallback:
                break
            continue
        if s.startswith(("#", "|", "---", "<!--")) or s.startswith("!["):
            continue
        if s.startswith(">"):
            fallback.append(s.lstrip("> ").strip())
            continue
        if s.startswith(("- ", "* ", "+ ")):
            fallback.append(s.lstrip("-*+ ").strip())
            continue
        primary.append(s)
        if len(" ".join(primary)) > 260:
            break

    if primary:
        text = strip_md(" ".join(primary))
    elif fallback:
        text = strip_md(" ".join(fallback))
    else:
        text = ""
    if text:
        return truncate(text)
    t = re.sub(r"^[\d.]+[\s.、]*", "", title).strip()
    return truncate(f"{t} 学习笔记与总结" if t else title)


def parse_front_matter(lines):
    start = None
    for i, ln in enumerate(lines):
        if ln.strip() == "---":
            start = i
            break
    if start is None:
        return None
    end = None
    for i in range(start + 1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None
    fm = lines[start + 1 : end]
    fields: dict[str, str] = {}
    cur = None
    for ln in fm:
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", ln)
        if m and not ln.startswith(" "):
            cur = m.group(1)
            fields[cur] = m.group(2).strip()
        elif cur and (ln.startswith(" ") or ln == "") and fields.get(cur):
            fields[cur] = (fields[cur] + " " + ln.strip()).strip()
    return start, end, fields


def yaml_quote(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def description_is_broken(desc: str) -> bool:
    d = desc.strip()
    return d.startswith('">') or d.startswith('" >') or d.startswith(">") or d == '""'


def process(path: str) -> str | None:
    with io.open(path, "r", encoding="utf-8", newline="") as f:
        text = f.read()

    # Mixed-newline safe: split on \n and strip \r
    lines = [ln.rstrip("\r") for ln in text.split("\n")]
    if lines and lines[-1] == "":
        lines.pop()  # drop trailing empty from final newline

    while lines and lines[0].strip() == "":
        lines.pop(0)

    parsed = parse_front_matter(lines)
    if parsed is None:
        return None
    start, end, fields = parsed

    existing = fields.get("description")
    if existing and not description_is_broken(existing):
        return None

    title = fields.get("title", os.path.splitext(os.path.basename(path))[0])
    summary = fields.get("summary")
    body = lines[end + 1 :]
    if summary:
        desc = truncate(strip_md(re.sub(r"^>\s*", "", summary.strip())))
    else:
        desc = first_paragraph(body, title)
    if not desc:
        return None

    # Insert/replace the description line right after the opening `---`
    if existing:
        # remove the old description line(s)
        out = []
        skipping = False
        for ln in lines:
            if ln.startswith("description:"):
                skipping = True
                continue
            if skipping and (ln.startswith(" ") or ln == ""):
                continue
            skipping = False
            out.append(ln)
        lines = out
        start = next(i for i, ln in enumerate(lines) if ln.strip() == "---")
    lines.insert(start + 1, "description: " + yaml_quote(desc))

    # Dominant newline
    nl = "\r\n" if text.count("\r\n") >= text.count("\n") - text.count("\r\n") else "\n"
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(nl.join(lines) + nl)
    return os.path.relpath(path, POSTS_ROOT)


def main() -> None:
    changed = 0
    for root, _dirs, files in os.walk(POSTS_ROOT):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            r = process(os.path.join(root, fn))
            if r is None:
                continue
            changed += 1
            print("ADDED/FIXED", r)
    print(f"\nchanged={changed}")


if __name__ == "__main__":
    main()
