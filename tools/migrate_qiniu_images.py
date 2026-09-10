# -*- coding: utf-8 -*-
"""Download all qiniu.kanes.top images to source/images/qiniu/.

Reads the URL list (one encoded absolute URL per line) from the file given
as argv[1], downloads each over plain http (the https cert expired), saves
under source/images/qiniu/ with the URL-decoded filename, and prints a
summary plus any failures. Re-runnable: existing non-empty files are kept.
"""
import sys
import os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote, quote
from urllib.request import urlopen, Request

URLS_FILE = sys.argv[1] if len(sys.argv) > 1 else "/tmp/qiniu_all.txt"
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "source", "images", "qiniu")
os.makedirs(OUT_DIR, exist_ok=True)

with open(URLS_FILE, encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

ok, skip, fail = 0, 0, []
lock_results = []

def fetch(url):
    name = unquote(url.rsplit("/", 1)[-1])
    dest = os.path.join(OUT_DIR, name)
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return ("skip", url, 0)
    http_url = quote(url.replace("https://", "http://", 1), safe=":/?=&%")
    last_err = None
    for _ in range(2):
        try:
            req = Request(http_url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req, timeout=30) as r:
                data = r.read()
            if len(data) < 64:
                raise RuntimeError("suspiciously small body: %d bytes" % len(data))
            with open(dest, "wb") as w:
                w.write(data)
            return ("ok", url, len(data))
        except Exception as e:
            last_err = e
    return ("fail", url, str(last_err))

with ThreadPoolExecutor(max_workers=8) as ex:
    lock_results = list(ex.map(fetch, urls))

total_bytes = 0
for status, url, info in lock_results:
    if status == "ok":
        ok += 1
        total_bytes += info
    elif status == "skip":
        skip += 1
    else:
        fail.append((url, info))

print("downloaded=%d skipped=%d failed=%d total=%.1fMB" % (ok, skip, len(fail), total_bytes / 1048576))
for url, err in fail:
    print("FAIL", url, err)
