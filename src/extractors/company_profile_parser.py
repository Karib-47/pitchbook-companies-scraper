from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)

def _safe_int(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None
    try:
        cleaned = "".join(ch for ch in value if ch.isdigit())
        return int(cleaned) if cleaned else None
    except (TypeError, ValueError):
        return None

def _extract_ld_json(soup: BeautifulSoup) -> Dict[str, Any]:
    """
    Try to extract a JSON-LD block describing the organization / company.
    """
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
        except (TypeError, json.JSONDecodeError):
            continue
        if isinstance(data, dict):
            if data.get("@type") in {"Organization", "Corporation"}:
                return data
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and item.get("@type") in {
                    "Organization",
                    "Corporation",
                }:
                    return item
    return {}

def _find_text(soup: BeautifulSoup, selectors: List[Dict[str, str]]) -> Optional[str]:
    for sel in selectors:
        tag = soup.find(sel.get("name"), attrs=sel.get("attrs"))
        if tag and tag.get_text(strip=True):
            return tag.get_text(strip=True)
    return None

def parse_company_profile(html: str, url: str) -> Dict[str, Any]:
    """
    Parse a PitchBook company profile HTML into a basic dict.

    This function focuses on robust patterns and sensible defaults rather than
    being tightly coupled to any specific DOM structure.
    """
    soup = BeautifulSoup(html, "html.parser")
    ld = _extract_ld_json(soup)

    company_name = ld.get("name") if ld else None
    if not company_name:
        company_name = _find_text(
            soup,
            [
                {"name": "h1", "attrs": {"data-test": "company-name"}},
                {"name": "h1", "attrs": {"class": "company-name"}},
                {"name": "h1", "attrs": {}},
            ],
        )

    description = ld.get("description") if ld else None
    if not description:
        description = _find_text(
            soup,
            [
                {"name": "p", "attrs": {"data-test": "company-description"}},
                {"name": "p", "attrs": {"class": "company-description"}},
            ],
        )

    year_founded = None
    status = None
    employees: Optional[int] = None

    # Simple key/value style details often appear in definition lists or tables
    for row in soup.select("dl, table tr"):
        label = row.find(["dt", "th"])
        value = row.find(["dd", "td"])
        if not label or not value:
            continue
        label_text = label.get_text(strip=True).lower()
        value_text = value.get_text(strip=True)
        if "founded" in label_text and year_founded is None:
            year_founded = _safe_int(value_text)
        elif ("status" in label_text or "ownership" in label_text) and status is None:
            status = value_text
        elif "employees" in label_text and employees is None:
            employees = _safe_int(value_text)

    # Social links
    socials: List[Dict[str, str]] = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        lower = href.lower()
        if any(domain in lower for domain in ("facebook.com", "linkedin.com", "twitter.com", "x.com")):
            domain = href.split("/")[2] if "://" in href else href
            socials.append({"domain": domain, "link": href})

    # Contact / metadata list (very generic)
    contact_information: List[Dict[str, str]] = []
    for li in soup.select("ul li[data-type], ul li[data-label]"):
        type_ = li.get("data-type") or li.get("data-label") or "Unknown"
        value = li.get_text(strip=True)
        if value:
            contact_information.append({"Type": type_, "value": value})

    basics: Dict[str, Any] = {
        "url": url,
        "id": ld.get("@id") or None,
        "company_name": company_name,
        "company_socials": socials,
        "year_founded": year_founded,
        "status": status,
        "employees": employees,
        "latest_deal_type": None,
        "financing_rounds": None,
        "investments": None,
        "description": description,
        "contact_information": contact_information,
        "patents": None,
        "research_analysis": None,
        "patent_activity": None,
    }

    LOGGER.debug("Parsed basic company profile for %s: %s", url, basics)
    return basics