#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

URL = "https://www.schulen-online.at/sol/oeff_suche_schulen.jsf"
OUT = Path("out")
OUT.mkdir(exist_ok=True)

s = requests.Session()
s.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
    "Accept-Language": "de-AT,de;q=0.9,en;q=0.5",
})

r = s.get(URL, timeout=60)
r.raise_for_status()
(OUT / "school-form.html").write_text(r.text, encoding="utf-8")
soup = BeautifulSoup(r.text, "lxml")
form = soup.find("form", id="myform1")
assert form is not None, "myform1 not found"

data: dict[str, str] = {}
for tag in form.find_all(["input", "select"], attrs={"name": True}):
    name = tag.get("name")
    if tag.name == "select":
        selected = tag.find("option", selected=True) or tag.find("option")
        data[name] = selected.get("value", "") if selected else ""
        continue
    typ = (tag.get("type") or "text").lower()
    if typ in {"submit", "button", "image", "file"}:
        continue
    if typ in {"checkbox", "radio"} and not tag.has_attr("checked"):
        continue
    data[name] = tag.get("value", "")

data.update({
    "myform1:skz": "",
    "myform1:bez": "",
    "myform1:schulart": "UNDEFINED",
    "myform1:art": "",
    "myform1:plz": "",
    "myform1:ort": "",
    "myform1:strasse": "",
    "myform1:bundesland": "-1",
    "myform1:bezirke": "-1",
    "myform1:sort": "0",
    "myform1:anz": "50",
    "myform1:j_id_1x": "Suchen",
    "myform1_SUBMIT": "1",
})

action = urljoin(URL, form.get("action") or URL)
print("GET", r.status_code, len(r.content), r.url)
print("POST", action)
print("DATA", json.dumps(data, ensure_ascii=False, indent=2))

r2 = s.post(action, data=data, timeout=120, allow_redirects=True)
print("RESULT", r2.status_code, len(r2.content), r2.url, r2.history)
r2.raise_for_status()
(OUT / "school-result.html").write_text(r2.text, encoding="utf-8")
rs = BeautifulSoup(r2.text, "lxml")
print("TITLE", rs.title.get_text(" ", strip=True) if rs.title else "")
print("SKZ", len(rs.select("div.skz")))
print("H1/H2", [h.get_text(" ", strip=True) for h in rs.find_all(["h1", "h2"])][:20])
print("ERRORS", [e.get_text(" ", strip=True) for e in rs.select(".error, .errors, .message, .messages, .ui-messages")])
print("TEXT", rs.get_text(" ", strip=True)[:3000])

for div in rs.select("div.skz")[:5]:
    a = div.find("a")
    print("ITEM", div.get_text(" ", strip=True), a.get("href") if a else None, a.get("onclick") if a else None)

for a in rs.find_all("a"):
    text = a.get_text(" ", strip=True)
    ident = " ".join(filter(None, [a.get("id"), a.get("name"), a.get("class") and " ".join(a.get("class"))]))
    if any(x in text.casefold() for x in ["vorwärts", "weiter", "next"]) or "next" in ident.casefold():
        print("NEXT", text, a.get("href"), a.get("onclick"), ident)
