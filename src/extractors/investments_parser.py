from __future__ import annotations

import logging
from dataclasses import asdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup

from src.models.investment_record import InvestmentRecord

LOGGER = logging.getLogger(__name__)

def _parse_date(value: str) -> Optional[str]:
    value = value.strip()
    # Try a few common formats, return ISO string or None
    for fmt in ("%Y-%m-%d", "%d %b %Y", "%b %d, %Y", "%Y"):
        try:
            dt = datetime.strptime(value, fmt)
            return dt.isoformat()
        except ValueError:
            continue
    return None

def parse_investments(html: str) -> tuple[Dict[str, Any], List[Dict[str, Any]], List[str]]:
    """
    Parse investment history and summary metrics.

    Returns:
      - summary dict with latest_deal_type, financing_rounds, investments
      - list of investment record dicts
      - list of investor names
    """
    soup = BeautifulSoup(html, "html.parser")

    investments: List[InvestmentRecord] = []
    investors: List[str] = []

    # Look for a generic investments table
    table = None
    for candidate in soup.find_all("table"):
        header_cells = [c.get_text(strip=True).lower() for c in candidate.find_all("th")]
        if not header_cells:
            continue
        if any("deal" in h for h in header_cells) and any("company" in h or "target" in h for h in header_cells):
            table = candidate
            break

    if table:
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) < 3:
                continue
            company_name = cells[0].get_text(strip=True) or None
            raw_date = cells[1].get_text(strip=True)
            deal_date = _parse_date(raw_date)
            raw_deal_size = cells[2].get_text(strip=True) or None
            deal_size = None
            if raw_deal_size:
                # Strip non-numeric, keep simple string so downstream code can interpret
                deal_size = raw_deal_size

            deal_type = None
            industry = None
            if len(cells) > 3:
                deal_type = cells[3].get_text(strip=True) or None
            if len(cells) > 4:
                industry = cells[4].get_text(strip=True) or None

            record = InvestmentRecord(
                company_name=company_name,
                deal_date=deal_date,
                deal_size=deal_size,
                deal_type=deal_type,
                industry=industry,
            )
            investments.append(record)

    # Basic metrics from summary badges or stats
    summary: Dict[str, Any] = {
        "latest_deal_type": None,
        "financing_rounds": len(investments) if investments else None,
        "investments": len(investments) if investments else None,
    }

    badge_container = soup.find(attrs={"data-test": "deal-summary"})
    if badge_container:
        badges = badge_container.find_all("span")
        for badge in badges:
            text = badge.get_text(strip=True).lower()
            if "latest" in text and "deal" in text and ":" in text:
                summary["latest_deal_type"] = text.split(":", 1)[1].strip()

    if investments and summary["latest_deal_type"] is None:
        summary["latest_deal_type"] = investments[0].deal_type

    # Investors list
    investor_section = soup.find(attrs={"data-test": "investors"})
    if investor_section:
        for tag in investor_section.find_all("a"):
            name = tag.get_text(strip=True)
            if name:
                investors.append(name)

    investments_dicts = [asdict(inv) for inv in investments]
    LOGGER.debug(
        "Parsed investments: %d records, summary=%s, investors=%d",
        len(investments_dicts),
        summary,
        len(investors),
    )
    return summary, investments_dicts, investors