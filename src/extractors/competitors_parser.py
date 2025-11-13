from __future__ import annotations

import logging
from typing import Any, Dict, List

from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)

def parse_competitors(html: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    competitors: List[Dict[str, Any]] = []

    table = None
    for candidate in soup.find_all("table"):
        header_cells = [c.get_text(strip=True).lower() for c in candidate.find_all("th")]
        if not header_cells:
            continue
        if any("competitor" in h or "company" in h for h in header_cells) and any(
            "location" in h for h in header_cells
        ):
            table = candidate
            break

    if not table:
        LOGGER.debug("No competitor table found.")
        return competitors

    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 3:
            continue
        name_cell = cells[0]
        status_cell = cells[1]
        location_cell = cells[2]

        link_tag = name_cell.find("a", href=True)
        link = link_tag["href"] if link_tag else None
        name = name_cell.get_text(strip=True) or None
        status = status_cell.get_text(strip=True) or None
        location = location_cell.get_text(strip=True) or None

        if not name:
            continue

        competitors.append(
            {
                "company_name": name,
                "financing_status": status,
                "link": link,
                "location": location,
            }
        )

    LOGGER.debug("Parsed %d competitors", len(competitors))
    return competitors