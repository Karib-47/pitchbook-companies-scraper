from __future__ import annotations

import logging
from typing import Any, Dict, List

from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)

def parse_faq(html: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    faq_entries: List[Dict[str, Any]] = []

    container = None
    # Try a few structural patterns
    for candidate in soup.find_all(attrs={"data-test": "faq-section"}):
        container = candidate
        break
    if not container:
        for candidate in soup.find_all("section"):
            heading = candidate.find(["h2", "h3"])
            if heading and "faq" in heading.get_text(strip=True).lower():
                container = candidate
                break

    if not container:
        LOGGER.debug("No FAQ section found.")
        return faq_entries

    # Q/A might be grouped in blocks
    for block in container.find_all(attrs={"data-test": "faq-item"}) or container.find_all("div"):
        question = None
        answer = None
        q_tag = block.find(["h3", "h4"], attrs={"data-test": "faq-question"}) or block.find(
            ["h3", "h4"], string=lambda s: s and "?" in s
        )
        a_tag = block.find("p", attrs={"data-test": "faq-answer"}) or block.find("p")
        if q_tag:
            question = q_tag.get_text(strip=True)
        if a_tag:
            answer = a_tag.get_text(strip=True)

        if question:
            faq_entries.append({"type": "Question", "value": question})
        if answer:
            faq_entries.append({"type": "Answer", "value": answer})

    LOGGER.debug("Parsed %d FAQ entries", len(faq_entries))
    return faq_entries