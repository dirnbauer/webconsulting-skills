#!/usr/bin/env python3
"""Build the current Austrian municipality master and resolve municipal websites.

The municipality master is authoritative Statistik Austria data. Website URLs are
supplemented from OpenStreetMap relation tags and linked Wikidata entities. These
supplementary URLs retain their source and are never guessed from a place name.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
import shapefile  # type: ignore

OUT = Path("municipality-export")
OUT.mkdir(exist_ok=True)
RAW = OUT / "raw"
RAW.mkdir(exist_ok=True)
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
UA = "webconsulting.at Austrian public website register/0.1 (contact: office@webconsulting.at)"
SHAPE_URL = (
    "https://www.statistik.gv.at/gs-open/GEODATA/ows?service=WFS&version=1.0.0"
    "&request=GetFeature&typeName=GEODATA:STATISTIK_AUSTRIA_GEM_20260101"
    "&outputFormat=SHAPE-ZIP&format_options=CHARSET:UTF-8"
)
META_URL = "https://data.statistik.gv.at/web/meta.jsp?dataset=OGDEXT_GEM_1"
STATES = {"1":"Burgenland","2":"Kärnten","3":"Niederösterreich","4":"Oberösterreich","5":"Salzburg","6":"Steiermark","7":"Tirol","8":"Vorarlberg","9":"Wien"}


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\u00a0", " ")).strip()


def norm(value: str) -> str:
    value = unicodedata.normalize("NFKD", clean(value).casefold())
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = value.replace("st.", "sankt").replace("st ", "sankt ")
    value = re.sub(r"\b(stadtgemeinde|marktgemeinde|gemeinde|stadt)\b", " ", value)
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def canonical_url(value: str) -> str:
    value = clean(value).strip(".,;()[]<>\"'")
    if not value:
        return ""
    if value.startswith("//"):
        value = "https:" + value
    elif value.startswith("www."):
        value = "https://" + value
    elif not re.match(r"^https?://", value, re.I) and re.match(r"^[A-Za-z0-9ÄÖÜäöüß.-]+\.[A-Za-z]{2,}(?:/|$)", value):
        value = "https://" + value
    try:
        parsed = urllib.parse.urlsplit(value)
    except Exception:
        return ""
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        return ""
    path = re.sub(r"/{2,}", "/", parsed.path or "/")
    return urllib.parse.urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, parsed.query, ""))


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


def request(session: requests.Session, method: str, url: str, attempts: int = 4, **kwargs: Any) -> requests.Response:
    last: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            response = session.request(method, url, timeout=240, **kwargs)
            if response.status_code in {429, 500, 502, 503, 504} and attempt < attempts:
                time.sleep(attempt * 5)
                continue
            response.raise_for_status()
            return response
        except Exception as exc:  # noqa: BLE001
            last = exc
            if attempt < attempts:
                time.sleep(attempt * 5)
    raise RuntimeError(f"Request failed: {url}: {last}")


def municipality_master(session: requests.Session) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    response = request(session, "GET", SHAPE_URL)
    (RAW / "municipalities-shape.zip").write_bytes(response.content)
    extract_dir = RAW / "municipalities-shape"
    extract_dir.mkdir(exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
        archive.extractall(extract_dir)
    shp = next(extract_dir.glob("*.shp"))
    reader = shapefile.Reader(str(shp), encoding="utf-8")
    fields = [field[0] for field in reader.fields[1:]]
    municipalities: list[dict[str, Any]] = []
    vienna_districts: list[dict[str, Any]] = []
    for record in reader.iterRecords():
        props = dict(zip(fields, record, strict=False))
        code = clean(props.get("g_id") or props.get("G_ID") or props.get("ID")).zfill(5)
        name = clean(props.get("g_name") or props.get("G_NAME") or props.get("NAME"))
        if not code or not name:
            continue
        if code.startswith("9"):
            vienna_districts.append({
                "organization_id": f"AT-WIEN-BEZ-{code[1:3]}",
                "official_id": code,
                "name": name,
                "organization_type": "municipal_district",
                "organization_type_label": "Wiener Gemeindebezirk",
                "administrative_level": "municipal_district",
                "federal_state": "Wien",
                "parent_organization_id": "AT-GEM-90001",
                "source_id": "SRC-STATAT-GEM-2026",
                "source_url": META_URL,
                "source_as_of": "2026-01-01",
                "retrieved_at": NOW,
            })
            continue
        municipalities.append(base_row(code, name))
    municipalities.append(base_row("90001", "Wien", note="Wien is represented by 23 district geometries in the GIS source and is consolidated here as one municipality."))
    municipalities = sorted({row["municipality_code"]: row for row in municipalities}.values(), key=lambda row: row["municipality_code"])
    if len(municipalities) != 2092:
        raise RuntimeError(f"Expected 2,092 municipalities, got {len(municipalities)}")
    return municipalities, sorted(vienna_districts, key=lambda row: row["official_id"])


def base_row(code: str, name: str, note: str = "") -> dict[str, Any]:
    return {
        "organization_id": f"AT-GEM-{code}",
        "official_id": code,
        "name": name,
        "organization_type": "municipality",
        "organization_type_label": "Gemeinde / Bundesland" if code == "90001" else "Gemeinde",
        "administrative_level": "municipal_state" if code == "90001" else "municipal",
        "federal_state": STATES.get(code[:1], ""),
        "district": "",
        "municipality_code": code,
        "school_code": "",
        "parent_organization_id": "",
        "ownership_control": "public",
        "legal_form": "Gebietskörperschaft",
        "active": True,
        "source_id": "SRC-STATAT-GEM-2026",
        "source_url": META_URL,
        "source_record_url": SHAPE_URL,
        "source_as_of": "2026-01-01",
        "retrieved_at": NOW,
        "notes": note,
    }


def overpass_relations(session: requests.Session) -> list[dict[str, Any]]:
    query = """[out:json][timeout:300];
area[\"ISO3166-1\"=\"AT\"][admin_level=2]->.a;
relation[\"boundary\"=\"administrative\"][\"admin_level\"=\"8\"](area.a);
out tags;"""
    endpoints = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
        "https://overpass.nchc.org.tw/api/interpreter",
    ]
    errors: list[str] = []
    for endpoint in endpoints:
        try:
            response = request(session, "POST", endpoint, attempts=2, data={"data": query})
            data = response.json()
            (RAW / "overpass-municipalities.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            return [element for element in data.get("elements", []) if element.get("type") == "relation"]
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{endpoint}: {exc}")
    (RAW / "overpass-errors.txt").write_text("\n".join(errors), encoding="utf-8")
    return []


def wikidata_websites(session: requests.Session, qids: list[str]) -> dict[str, str]:
    websites: dict[str, str] = {}
    api = "https://www.wikidata.org/w/api.php"
    for index in range(0, len(qids), 50):
        batch = qids[index:index + 50]
        try:
            response = request(session, "GET", api, attempts=3, params={
                "action": "wbgetentities",
                "ids": "|".join(batch),
                "props": "claims|labels",
                "languages": "de|en",
                "format": "json",
            })
            entities = response.json().get("entities", {})
            for qid, entity in entities.items():
                claims = entity.get("claims", {}).get("P856", [])
                for claim in claims:
                    value = claim.get("mainsnak", {}).get("datavalue", {}).get("value")
                    url = canonical_url(value)
                    if url:
                        websites[qid] = url
                        break
        except Exception:
            continue
        time.sleep(0.05)
    return websites


def resolve_websites(session: requests.Session, municipalities: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    by_code = {row["municipality_code"]: row for row in municipalities}
    by_name: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in municipalities:
        by_name[norm(row["name"])].append(row)
    relations = overpass_relations(session)
    qids = sorted({clean(element.get("tags", {}).get("wikidata")) for element in relations if clean(element.get("tags", {}).get("wikidata"))})
    wikidata = wikidata_websites(session, qids)
    websites: list[dict[str, Any]] = []
    unmatched: list[dict[str, Any]] = []
    matched_codes: set[str] = set()
    for element in relations:
        tags = element.get("tags", {}) or {}
        code_candidates = [
            clean(tags.get("ref:at:gkz")),
            clean(tags.get("ref:at:gemeindekennziffer")),
            clean(tags.get("de:amtlicher_gemeindeschluessel")),
            clean(tags.get("ref")),
        ]
        code = ""
        municipality: dict[str, Any] | None = None
        for candidate in code_candidates:
            digits = re.sub(r"\D", "", candidate)
            if len(digits) >= 5 and digits[-5:] in by_code:
                code = digits[-5:]
                municipality = by_code[code]
                break
        if municipality is None:
            candidates = by_name.get(norm(clean(tags.get("name"))), [])
            if len(candidates) == 1:
                municipality = candidates[0]
                code = municipality["municipality_code"]
        if municipality is None:
            unmatched.append({"osm_relation_id": element.get("id"), "name": clean(tags.get("name")), "tags": json.dumps(tags, ensure_ascii=False)})
            continue
        url = ""
        source_id = ""
        source_url = ""
        for key in ("contact:website", "website", "official_website", "url"):
            url = canonical_url(clean(tags.get(key)))
            if url:
                source_id = "SRC-OSM-MUNICIPALITY"
                source_url = f"https://www.openstreetmap.org/relation/{element.get('id')}"
                break
        qid = clean(tags.get("wikidata"))
        if not url and qid:
            url = wikidata.get(qid, "")
            if url:
                source_id = "SRC-WIKIDATA-MUNICIPALITY"
                source_url = f"https://www.wikidata.org/wiki/{qid}"
        if not url:
            continue
        matched_codes.add(code)
        domain = urllib.parse.urlsplit(url).netloc.lower().removeprefix("www.")
        website_id = "AT-WEB-" + hashlib.sha1(f"{municipality['organization_id']}|{url}".encode()).hexdigest()[:12].upper()
        websites.append({
            "website_id": website_id,
            "organization_id": municipality["organization_id"],
            "url": url,
            "domain": domain,
            "presence_type": "own_domain" if urllib.parse.urlsplit(url).path in {"", "/"} else "website_or_subpage",
            "is_primary": True,
            "verification_status": "supplementary_directory_match_by_official_code_or_unique_name",
            "source_id": source_id,
            "source_url": source_url,
            "retrieved_at": NOW,
            "notes": f"OSM relation {element.get('id')}; Wikidata {qid}".strip("; "),
        })
    # Wien is guaranteed to have a current official municipal portal even when
    # the admin-level query represents it differently.
    if "90001" not in matched_codes:
        url = "https://www.wien.gv.at/"
        websites.append({
            "website_id": "AT-WEB-GEM-90001",
            "organization_id": "AT-GEM-90001",
            "url": url,
            "domain": "wien.gv.at",
            "presence_type": "own_domain",
            "is_primary": True,
            "verification_status": "official_portal_manual_seed",
            "source_id": "SRC-WIEN-OFFICIAL",
            "source_url": url,
            "retrieved_at": NOW,
            "notes": "",
        })
    websites = sorted({(row["organization_id"], row["url"]): row for row in websites}.values(), key=lambda row: row["organization_id"])
    return websites, {
        "overpass_relations": len(relations),
        "wikidata_entities_requested": len(qids),
        "unmatched_relations": len(unmatched),
        "municipalities_with_website": len({row["organization_id"] for row in websites}),
        "unmatched_sample": unmatched[:100],
    }


def main() -> int:
    session = requests.Session()
    session.headers.update({"User-Agent": UA, "Accept-Language": "de-AT,de;q=0.9,en;q=0.5"})
    municipalities, districts = municipality_master(session)
    websites, supplemental = resolve_websites(session, municipalities)
    write_csv(OUT / "municipalities.csv", municipalities)
    write_csv(OUT / "vienna-municipal-districts.csv", districts)
    write_csv(OUT / "municipality-websites.csv", websites)
    coverage = {
        "generated_at": NOW,
        "municipalities": len(municipalities),
        "municipalities_by_state": dict(Counter(row["federal_state"] for row in municipalities)),
        "vienna_municipal_districts": len(districts),
        "websites": len(websites),
        "unique_domains": len({row["domain"] for row in websites}),
        **supplemental,
        "source_note": "Statistik Austria is authoritative for the municipality master. OSM/Wikidata are supplementary website sources and retain verification metadata.",
    }
    (OUT / "coverage.json").write_text(json.dumps(coverage, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(coverage, ensure_ascii=False), flush=True)
    return 0 if len(municipalities) == 2092 else 1


if __name__ == "__main__":
    sys.exit(main())
