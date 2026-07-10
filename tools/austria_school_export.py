#!/usr/bin/env python3
"""Export every public entry from Austria's national Schulen-Online directory."""
from __future__ import annotations

import csv
import json
import re
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup, Tag

OUT = Path("school-export")
OUT.mkdir(exist_ok=True)
SEARCH = "https://www.schulen-online.at/sol/oeff_suche_schulen.jsf"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36"
STATES = {"1":"Burgenland","2":"Kärnten","3":"Niederösterreich","4":"Oberösterreich","5":"Salzburg","6":"Steiermark","7":"Tirol","8":"Vorarlberg","9":"Wien"}


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\u00a0", " ")).strip()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def canonical_url(value: str) -> str:
    value = clean(value).strip(".,;()[]<>\"'")
    if not value:
        return ""
    # Some directory entries contain explanatory text or more than one URL.
    match = re.search(r"(?:https?://|www\.)[^\s,;]+", value, re.I)
    if match:
        value = match.group(0)
    if value.startswith("www."):
        value = "https://" + value
    elif not re.match(r"^https?://", value, re.I) and re.match(r"^[A-Za-z0-9ÄÖÜäöüß.-]+\.[A-Za-z]{2,}", value):
        value = "https://" + value
    try:
        parsed = urllib.parse.urlsplit(value)
    except Exception:
        return ""
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        return ""
    path = re.sub(r"/{2,}", "/", parsed.path or "/")
    return urllib.parse.urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, parsed.query, ""))


def hidden_values(form: Tag) -> dict[str, str]:
    data: dict[str, str] = {}
    for field in form.find_all("input", attrs={"name": True}):
        kind = clean(field.get("type")).lower()
        if kind in {"submit", "button", "image", "file"}:
            continue
        if kind in {"checkbox", "radio"} and not field.has_attr("checked"):
            continue
        data[clean(field.get("name"))] = clean(field.get("value"))
    return data


def submit_search() -> tuple[requests.Session, str, requests.Response]:
    session = requests.Session()
    session.headers.update({"User-Agent": UA, "Accept-Language": "de-AT,de;q=0.9,en;q=0.5"})
    response = session.get(SEARCH, timeout=60)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    form = soup.find("form", id="myform1")
    if not isinstance(form, Tag):
        raise RuntimeError("Schulen-Online form myform1 not found")
    data = hidden_values(form)
    for select in form.find_all("select", attrs={"name": True}):
        selected = select.find("option", selected=True) or select.find("option")
        data[clean(select.get("name"))] = clean(selected.get("value")) if selected else ""
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
    action = urllib.parse.urljoin(response.url, clean(form.get("action")) or response.url)
    result = session.post(action, data=data, timeout=90)
    result.raise_for_status()
    return session, action, result


def post_target(session: requests.Session, action: str, page_html: str, target: str) -> requests.Response:
    soup = BeautifulSoup(page_html, "lxml")
    form = soup.find("form", id="j_id_20")
    if not isinstance(form, Tag):
        raise RuntimeError("Result form j_id_20 not found")
    data = hidden_values(form)
    data["j_id_20_SUBMIT"] = "1"
    data["j_id_20:_idcl"] = target
    response = session.post(action, data=data, timeout=90)
    response.raise_for_status()
    return response


def result_rows(page_html: str) -> tuple[list[dict[str, str]], int, int, int]:
    soup = BeautifulSoup(page_html, "lxml")
    rows: list[dict[str, str]] = []
    for tr in soup.select("#j_id_20\\:j_id_22\\:tbody_element tr"):
        anchor = tr.select_one("div.skz a")
        if not isinstance(anchor, Tag):
            continue
        quoted = re.findall(r"'([^']+)'", clean(anchor.get("onclick")))
        target = quoted[1] if len(quoted) >= 2 else ""
        cells = tr.find_all("td")
        rows.append({
            "school_code": clean(anchor.get_text(" ", strip=True)),
            "name_summary": clean(cells[1].get_text(" ", strip=True)) if len(cells) > 1 else "",
            "address_summary": clean(cells[2].get_text(" ", strip=True)) if len(cells) > 2 else "",
            "target": target,
        })
    def integer(selector: str) -> int:
        node = soup.select_one(selector)
        value = clean(node.get_text(" ", strip=True)) if node else "0"
        match = re.search(r"\d+", value)
        return int(match.group(0)) if match else 0
    return rows, integer("#j_id_20\\:from"), integer("#j_id_20\\:to"), integer("#j_id_20\\:sum")


def detail_labels(page_html: str) -> dict[str, str]:
    soup = BeautifulSoup(page_html, "lxml")
    labels: dict[str, str] = {}
    for heading in soup.select("#tabs-3 h5"):
        label = clean(heading.get_text(" ", strip=True))
        value_node = heading.find_next_sibling()
        labels[label] = clean(value_node.get_text(" ", strip=True)) if isinstance(value_node, Tag) else ""
    return labels


def split_address(address: str) -> tuple[str, str, str]:
    address = clean(address)
    match = re.match(r"^(\d{4})\s+([^,]+),\s*(.*)$", address)
    if match:
        return match.group(3), match.group(1), match.group(2)
    match = re.match(r"^(\d{4})\s+(.+)$", address)
    if match:
        return "", match.group(1), match.group(2)
    return address, "", ""


def normalize_record(summary: dict[str, str], labels: dict[str, str]) -> dict[str, Any]:
    code = re.sub(r"\D", "", labels.get("Schulkennzahl") or summary["school_code"])
    address = labels.get("Adresse") or summary["address_summary"]
    street, postal_code, locality = split_address(address)
    public_private = labels.get("öffentlich/privat", "")
    homepage_raw = labels.get("Homepage", "")
    homepage = canonical_url(homepage_raw)
    return {
        "organization_id": f"AT-SCH-{code}",
        "school_code": code,
        "name": labels.get("Titel") or summary["name_summary"],
        "school_types": labels.get("Schulart(en)") or summary["name_summary"],
        "address": address,
        "street_address": street,
        "postal_code": postal_code,
        "locality": locality,
        "federal_state": STATES.get(code[:1], "") if code else "",
        "public_private": public_private,
        "ownership_control": "private" if "privat" in public_private.casefold() else "public",
        "school_operator": labels.get("Schulerhalter", ""),
        "supervisory_authority": labels.get("Schulaufsichtsbehörde", ""),
        "day_care": labels.get("Schulische Tagesbetreuung", ""),
        "phone": labels.get("Telefon", ""),
        "fax": labels.get("Fax", ""),
        "email_administration": labels.get("E-Mail Verwaltung", ""),
        "email_pedagogy": labels.get("E-Mail Pädagogik", ""),
        "homepage_raw": homepage_raw,
        "homepage": homepage,
        "domain": urllib.parse.urlsplit(homepage).netloc.lower().removeprefix("www.") if homepage else "",
        "source_id": "SRC-BMB-SCHULENONLINE",
        "source_url": SEARCH,
        "retrieved_at": NOW,
        "detail_status": "complete" if labels.get("Schulkennzahl") else "summary_only",
    }


def main() -> int:
    session, action, response = submit_search()
    current_html = response.text
    schools: list[dict[str, Any]] = []
    seen: set[str] = set()
    page_number = 0
    expected_total = 0
    errors: list[dict[str, str]] = []
    started = time.time()

    while page_number < 300:
        page_number += 1
        rows, first, last, total = result_rows(current_html)
        expected_total = total or expected_total
        new_rows = [row for row in rows if row["school_code"] not in seen]
        print(f"Page {page_number}: {first}-{last} / {total}; new rows {len(new_rows)}", flush=True)
        if not new_rows:
            break

        for index, summary in enumerate(new_rows, start=1):
            labels: dict[str, str] = {}
            if summary["target"]:
                try:
                    detail = post_target(session, action, current_html, summary["target"])
                    current_html = detail.text
                    labels = detail_labels(current_html)
                except Exception as exc:  # noqa: BLE001
                    errors.append({"school_code": summary["school_code"], "error": clean(exc)})
            record = normalize_record(summary, labels)
            if record["school_code"] in seen:
                continue
            seen.add(record["school_code"])
            schools.append(record)
            if index % 10 == 0:
                print(f"  page {page_number}: detail {index}/{len(new_rows)}; total {len(schools)}", flush=True)

        write_csv(OUT / "schools-progress.csv", schools)
        (OUT / "errors-progress.json").write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")
        if total and last >= total:
            break
        try:
            next_page = post_target(session, action, current_html, "j_id_20:next")
            current_html = next_page.text
        except Exception as exc:  # noqa: BLE001
            errors.append({"school_code": "PAGE", "error": f"pagination after page {page_number}: {clean(exc)}"})
            break

    schools.sort(key=lambda row: row["school_code"])
    write_csv(OUT / "schools.csv", schools)
    websites = [
        {
            "website_id": f"AT-WEB-SCH-{row['school_code']}",
            "organization_id": row["organization_id"],
            "url": row["homepage"],
            "domain": row["domain"],
            "is_primary": True,
            "verification_status": "listed_by_official_directory",
            "source_id": row["source_id"],
            "source_url": row["source_url"],
            "retrieved_at": NOW,
        }
        for row in schools if row["homepage"]
    ]
    write_csv(OUT / "school-websites.csv", websites)
    coverage = {
        "generated_at": NOW,
        "expected_total": expected_total,
        "schools_exported": len(schools),
        "schools_with_homepage": len(websites),
        "unique_domains": len({row["domain"] for row in websites if row["domain"]}),
        "detail_complete": sum(row["detail_status"] == "complete" for row in schools),
        "errors": len(errors),
        "elapsed_seconds": round(time.time() - started, 1),
    }
    (OUT / "coverage.json").write_text(json.dumps(coverage, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "errors.json").write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(coverage, ensure_ascii=False), flush=True)
    return 0 if len(schools) >= max(1, expected_total - 10) else 1


if __name__ == "__main__":
    sys.exit(main())
