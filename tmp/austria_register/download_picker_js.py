#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

OUT = Path("out")
html_path = OUT / "picker.html"
if not html_path.exists():
    raise SystemExit("picker.html missing")

base = "https://www.oesterreich.gv.at/de/orgsearch/gemeindeauswahl/orgtypegroup/2"
soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "lxml")ns = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0"
for index, script in enumerate(soup.find_all("script", src=True), start=1):
    url = urljoin(base, script.get("src"))
    if "_next/static/chunks" not in url:
        continue
    r = s.get(url, timeout=90)
    print(index, r.status_code, len(r.content), url)
    r.raise_for_status()
    name = script.get("src").split("/")[-1]
    (OUT / f"picker-js-{index:02d}-{name}").write_bytes(r.content)
