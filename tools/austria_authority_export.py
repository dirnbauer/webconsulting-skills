#!/usr/bin/env python3
"""Export Austrian authorities and institution websites from oesterreich.gv.at."""
from __future__ import annotations

import csv
import hashlib
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

OUT = Path("authority-export")
RAW = OUT / "raw"
OUT.mkdir(exist_ok=True)
RAW.mkdir(exist_ok=True)
BASE = "https://www.oesterreich.gv.at/de/orgsearch"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36"
LEGACY_TYPES = {
    "1": "Agrarmarkt Austria",
    "5": "Österreichische Nationalbibliothek",
    "14": "Sozialversicherungsträger",
    "18": "Rechnungshof",
    "27": "Bundesdenkmalamt",
    "30": "Europäische und internationale Einrichtungen",
    "34": "Technisches Museum Wien",
    "39": "Weitere öffentliche und angeschlossene Stellen",
}
TYPE_CLASSIFICATION = {
    "Notrufnummern": ("emergency_contact", "service", "public"),
    "Servicenummern": ("public_service_contact", "service", "public"),
    "Arbeitsinspektion": ("labour_inspectorate", "federal", "public"),
    "Arbeitsmarktservice": ("employment_service", "federal", "public_law"),
    "Bezirkshauptmannschaft": ("district_authority", "district", "public"),
    "Bundesministerium": ("ministry", "federal", "public"),
    "Finanzamt": ("tax_authority", "federal", "public"),
    "Gemeindeamt/Magistrat": ("municipality_authority", "municipal", "public"),
    "Gericht": ("judiciary", "federal", "public"),
    "Landesregierung": ("state_authority", "state", "public"),
    "Polizei": ("police_authority", "federal", "public"),
    "Standesamt": ("registry_office", "municipal", "public"),
    "Verkehrsamt": ("transport_authority", "district", "public"),
    "Volksanwaltschaft": ("ombudsman", "federal", "public"),
    "Zollamt": ("customs_authority", "federal", "public"),
    "Agrarmarkt Austria": ("federal_agency", "federal", "public_law"),
    "Österreichische Nationalbibliothek": ("federal_cultural_institution", "federal", "public_law"),
    "Sozialversicherungsträger": ("social_insurance", "statutory", "public_law"),
    "Rechnungshof": ("audit_institution", "federal", "public"),
    "Bundesdenkmalamt": ("federal_agency", "federal", "public"),
    "Europäische und internationale Einrichtungen": ("international_public_body", "international", "public"),
    "Technisches Museum Wien": ("federal_cultural_institution", "federal", "public_law"),
    "Weitere öffentliche und angeschlossene Stellen": ("attached_public_body", "unknown", "public_or_attached"),
}


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


def stable_id(*parts: str) -> str:
    value = "|".join(clean(p).casefold() for p in parts)
    return "AT-ORG-" + hashlib.sha1(value.encode("utf-8")).hexdigest()[:12].upper()


def canonical_url(value: str) -> str:
    value = clean(value).strip(".,;()[]<>\"'")
    if value.startswith("www."):
        value = "https://" + value
    try:
        parsed = urllib.parse.urlsplit(value)
    except Exception:
        return ""
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return ""
    path = re.sub(r"/{2,}", "/", parsed.path or "/")
    return urllib.parse.urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, parsed.query, ""))


def discover_types(raw_html: str) -> dict[str, str]:
    pattern = re.compile(
        r'\{\\"id\\":(?P<id>\d+),\\"orgTypeIdList\\":.*?,'
        r'\\"title\\":\\"(?P<title>.*?)\\",\\"shortkey\\":\\".*?\\",'
        r'\\"regional\\":(?:true|false),\\"type\\":(?P<is_type>true|false)\}'
    )
    found: dict[str, str] = {}
    for match in pattern.finditer(raw_html):
        if match.group("is_type") == "true":
            title = bytes(match.group("title"), "utf-8").decode("unicode_escape")
            found[match.group("id")] = title
    found.update({key: value for key, value in LEGACY_TYPES.items() if key not in found})
    return found


def section_node(heading: Tag) -> Tag | None:
    sibling = heading.find_next_sibling()
    return sibling if isinstance(sibling, Tag) and sibling.name != "h2" else None


def parse_address(node: Tag | None) -> tuple[str, str, str]:
    if not node:
        return "", "", ""
    first = node.find("div")
    raw = "\n".join(first.stripped_strings) if isinstance(first, Tag) else ""
    lines = [clean(line) for line in raw.splitlines() if clean(line)]
    street = lines[0] if lines else ""
    postal = ""
    locality = ""
    for line in lines[1:]:
        match = re.match(r"^(\d{4})\s+(.+)$", line)
        if match:
            postal, locality = match.groups()
            break
    return street, postal, locality


def classify(label: str, name: str) -> tuple[str, str, str]:
    if label in TYPE_CLASSIFICATION:
        return TYPE_CLASSIFICATION[label]
    joined = f"{label} {name}".casefold()
    if "universität" in joined or "hochschule" in joined:
        return "higher_education", "federal", "public_or_private"
    if "kammer" in joined:
        return "chamber", "statutory", "public_law"
    if "fonds" in joined:
        return "public_fund", "unknown", "public_or_attached"
    if "agentur" in joined or "anstalt" in joined:
        return "public_agency", "unknown", "public_or_attached"
    return "public_body", "unknown", "public_or_attached"


def main() -> int:
    session = requests.Session()
    session.headers.update({"User-Agent": UA, "Accept-Language": "de-AT,de;q=0.9,en;q=0.5"})
    overview = session.get(BASE, timeout=60)
    overview.raise_for_status()
    (RAW / "orgsearch.html").write_bytes(overview.content)
    type_map = discover_types(overview.text)
    if not type_map:
        raise RuntimeError("No authority types discovered")

    organizations: list[dict[str, Any]] = []
    websites: list[dict[str, Any]] = []
    coverage_types: dict[str, dict[str, Any]] = {}
    for type_id, label in sorted(type_map.items(), key=lambda item: int(item[0])):
        url = f"{BASE}/orgtyp/{type_id}"
        try:
            response = session.get(url, timeout=90)
            response.raise_for_status()
        except Exception as exc:  # noqa: BLE001
            coverage_types[type_id] = {"label": label, "error": clean(exc), "entries": 0}
            continue
        (RAW / f"orgtyp-{type_id}.html").write_bytes(response.content)
        soup = BeautifulSoup(response.text, "lxml")
        headings = [
            h for h in soup.find_all("h2")
            if clean(h.get_text(" ", strip=True)).casefold()
            not in {"abfrageergebnis", "information", "behördensuche", "behörden- / personenverzeichnisse", "behörden-/personenverzeichnisse", "seite nicht gefunden"}
        ]
        coverage_types[type_id] = {"label": label, "entries": len(headings), "url": url}
        print(f"Type {type_id} {label}: {len(headings)}", flush=True)
        for heading in headings:
            name = clean(heading.get_text(" ", strip=True))
            node = section_node(heading)
            text = "\n".join(clean(x) for x in node.stripped_strings) if node else ""
            street, postal_code, locality = parse_address(node)
            email_links: list[str] = []
            phone_links: list[str] = []
            external_links: list[str] = []
            if node:
                for anchor in node.find_all("a", href=True):
                    href = clean(anchor.get("href"))
                    if href.startswith("mailto:"):
                        email_links.append(href[7:])
                    elif href.startswith("tel:"):
                        phone_links.append(href[4:])
                    else:
                        candidate = canonical_url(href)
                        host = urllib.parse.urlsplit(candidate).netloc.lower().removeprefix("www.") if candidate else ""
                        if candidate and host not in {"maps.google.com", "google.com", "route.bmk.gv.at", "oesterreich.gv.at"} and not host.endswith("google.com"):
                            external_links.append(candidate)
            org_type, level, ownership = classify(label, name)
            org_id = stable_id(type_id, name, street, postal_code, locality)
            organizations.append({
                "organization_id": org_id,
                "official_id": "",
                "name": name,
                "organization_type": org_type,
                "organization_type_label": label,
                "administrative_level": level,
                "federal_state": "",
                "district": "",
                "municipality_code": "",
                "school_code": "",
                "parent_organization_id": "",
                "ownership_control": ownership,
                "legal_form": "",
                "street_address": street,
                "postal_code": postal_code,
                "locality": locality,
                "email": "; ".join(dict.fromkeys(email_links)),
                "phone": "; ".join(dict.fromkeys(phone_links)),
                "active": True,
                "source_id": "SRC-OEGV-ORGSEARCH",
                "source_url": BASE,
                "source_record_url": url,
                "retrieved_at": NOW,
                "notes": clean(text) if not node else "",
            })
            for index, website in enumerate(dict.fromkeys(external_links), start=1):
                host = urllib.parse.urlsplit(website).netloc.lower().removeprefix("www.")
                websites.append({
                    "website_id": "AT-WEB-" + hashlib.sha1(f"{org_id}|{website}".encode()).hexdigest()[:12].upper(),
                    "organization_id": org_id,
                    "url": website,
                    "domain": host,
                    "presence_type": "own_domain" if urllib.parse.urlsplit(website).path in {"", "/"} else "website_or_subpage",
                    "is_primary": index == 1,
                    "verification_status": "listed_by_official_directory",
                    "source_id": "SRC-OEGV-ORGSEARCH",
                    "source_url": url,
                    "retrieved_at": NOW,
                })
        time.sleep(0.05)

    # Exact duplicates can occur where legacy and current type routes overlap.
    deduped: dict[tuple[str, str, str], dict[str, Any]] = {}
    aliases: dict[str, str] = {}
    for row in organizations:
        key = (row["name"].casefold(), row["postal_code"], row["street_address"].casefold())
        if key not in deduped:
            deduped[key] = row
        else:
            aliases[row["organization_id"]] = deduped[key]["organization_id"]
            labels = set(filter(None, [deduped[key]["organization_type_label"], row["organization_type_label"]]))
            deduped[key]["organization_type_label"] = "; ".join(sorted(labels))
    for website in websites:
        website["organization_id"] = aliases.get(website["organization_id"], website["organization_id"])
    organizations = sorted(deduped.values(), key=lambda row: (row["organization_type"], row["name"]))
    websites = sorted({(row["organization_id"], row["url"]): row for row in websites}.values(), key=lambda row: (row["organization_id"], row["url"]))
    write_csv(OUT / "authorities.csv", organizations)
    write_csv(OUT / "authority-websites.csv", websites)
    write_csv(OUT / "ministries.csv", [row for row in organizations if row["organization_type"] == "ministry"])
    coverage = {
        "generated_at": NOW,
        "authority_types": coverage_types,
        "organizations": len(organizations),
        "websites": len(websites),
        "unique_domains": len({row["domain"] for row in websites}),
        "ministries": sum(row["organization_type"] == "ministry" for row in organizations),
    }
    (OUT / "coverage.json").write_text(json.dumps(coverage, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(coverage, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
