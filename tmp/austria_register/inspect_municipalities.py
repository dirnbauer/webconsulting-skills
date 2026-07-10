#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

OUT = Path("out")
OUT.mkdir(exist_ok=True)
URLS = {
    "picker": "https://www.oesterreich.gv.at/de/orgsearch/gemeindeauswahl/orgtypegroup/2",
    "picker-a": "https://www.oesterreich.gv.at/de/orgsearch/gemeindeauswahl/orgtypegroup/2?q=A",
    "eisenstadt": "https://www.oesterreich.gv.at/de/orgsearch/orgtypegroup/2?gkz=10101",
    "gemeindebund": "https://gemeindebund.at/gemeinden/",
}

s = requests.Session()
s.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
    "Accept-Language": "de-AT,de;q=0.9,en;q=0.5",
})

for name, url in URLS.items():
    try:
        r = s.get(url, timeout=90, allow_redirects=True)
        print(name, r.status_code, len(r.content), r.url, r.headers.get("content-type"))
        r.raise_for_status()
    except Exception as exc:
        print(name, "ERROR", repr(exc))
        continue
    path = OUT / f"{name}.html"
    path.write_bytes(r.content)
    text = r.text
    soup = BeautifulSoup(text, "lxml")
    print(name, "title", soup.title.get_text(" ", strip=True) if soup.title else "")
    print(name, "scripts", len(soup.find_all("script")))
    print(name, "headings", [h.get_text(" ", strip=True) for h in soup.find_all(["h1", "h2", "h3"])][:40])
    for script in soup.find_all("script", src=True):
        print(name, "SCRIPT", urljoin(r.url, script.get("src")))
    for term in ["api", "autocomplete", "municip", "gemeinde", "orgsearch", "suggest", "search", "__next_f.push", "wp-json", "gkz", "regions", "homepage"]:
        positions = [m.start() for m in re.finditer(term, text, re.I)][:5]
        print(name, "TERM", term, positions)
        for pos in positions[:2]:
            print(text[max(0, pos - 250):pos + 700].replace("\n", " "))
    urls = sorted(set(re.findall(r"https?://[^\"'<>\\\s]+", text)))
    (OUT / f"{name}-urls.json").write_text(json.dumps(urls, ensure_ascii=False, indent=2), encoding="utf-8")
    print(name, "embedded urls", len(urls))
