#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

URL = "https://www.schulen-online.at/sol/oeff_suche_schulen.jsf"
OUT = Path("out")
OUT.mkdir(exist_ok=True)

s = requests.Session()
s.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
    "Accept-Language": "de-AT,de;q=0.9,en;q=0.5",
})


def view_state(soup: BeautifulSoup) -> str:
    tag = soup.find("input", attrs={"name": "javax.faces.ViewState"})
    assert isinstance(tag, Tag), "ViewState missing"
    return tag.get("value", "")


def jsf_post(target: str, soup: BeautifulSoup) -> BeautifulSoup:
    payload = {
        "j_id_20_SUBMIT": "1",
        "javax.faces.ViewState": view_state(soup),
        "j_id_20:_idcl": target,
    }
    result = s.post(URL, data=payload, timeout=120)
    print("JSF", target, result.status_code, len(result.content), result.url)
    result.raise_for_status()
    return BeautifulSoup(result.text, "lxml")


r = s.get(URL, timeout=60)
r.raise_for_status()
(OUT / "school-form.html").write_text(r.text, encoding="utf-8")
soup = BeautifulSoup(r.text, "lxml")
form = soup.find("form", id="myform1")
assert isinstance(form, Tag), "myform1 not found"

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
print("SKZ", len(rs.select("div.skz")))

first = rs.select_one("div.skz a")
assert isinstance(first, Tag), "No first school link"
onclick = first.get("onclick", "")
quoted = re.findall(r"['\"]([^'\"]+)['\"]", onclick)
assert len(quoted) >= 2, onclick
target = quoted[1]
print("FIRST TARGET", target)
detail = jsf_post(target, rs)
(OUT / "school-detail.html").write_text(str(detail), encoding="utf-8")
print("DETAIL BOXES", len(detail.select("div.anzeigefeld")))
print("DETAIL TEXT", detail.get_text(" | ", strip=True)[-5000:])
for box_index, box in enumerate(detail.select("div.anzeigefeld")):
    print("BOX", box_index, box.get_text(" | ", strip=True))
    for a in box.find_all("a", href=True):
        print("  LINK", a.get_text(" ", strip=True), a.get("href"))

next_page = jsf_post("j_id_20:next", detail)
(OUT / "school-page-2.html").write_text(str(next_page), encoding="utf-8")
print("PAGE2 CODES", [x.get_text(" ", strip=True) for x in next_page.select("div.skz")[:5]])
