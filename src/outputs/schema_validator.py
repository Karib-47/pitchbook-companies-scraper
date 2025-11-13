from __future__ import annotations

import logging
from typing import Any, Dict, Iterable, List

from jsonschema import Draft7Validator

LOGGER = logging.getLogger(__name__)

SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "url": {"type": "string"},
        "id": {"type": ["string", "null"]},
        "company_name": {"type": ["string", "null"]},
        "company_socials": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "domain": {"type": "string"},
                    "link": {"type": "string"},
                },
                "required": ["domain", "link"],
            },
        },
        "year_founded": {"type": ["integer", "null"]},
        "status": {"type": ["string", "null"]},
        "employees": {"type": ["integer", "null"]},
        "latest_deal_type": {"type": ["string", "null"]},
        "financing_rounds": {"type": ["integer", "null"]},
        "investments": {"type": ["integer", "null"]},
        "description": {"type": ["string", "null"]},
        "contact_information": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "Type": {"type": "string"},
                    "value": {"type": "string"},
                },
                "required": ["Type", "value"],
            },
        },
        "patents": {},
        "competitors": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "company_name": {"type": ["string", "null"]},
                    "financing_status": {"type": ["string", "null"]},
                    "link": {"type": ["string", "null"]},
                    "location": {"type": ["string", "null"]},
                },
                "required": ["company_name", "financing_status", "link", "location"],
            },
        },
        "research_analysis": {},
        "patent_activity": {},
        "all_investments": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "company_name": {"type": ["string", "null"]},
                    "deal_date": {"type": ["string", "null"]},
                    "deal_size": {"type": ["string", "null"]},
                    "deal_type": {"type": ["string", "null"]},
                    "industry": {"type": ["string", "null"]},
                },
                "required": [
                    "company_name",
                    "deal_date",
                    "deal_size",
                    "deal_type",
                    "industry",
                ],
            },
        },
        "faq": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "value": {"type": "string"},
                },
                "required": ["type", "value"],
            },
        },
        "investors": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": [
        "url",
        "id",
        "company_name",
        "company_socials",
        "year_founded",
        "status",
        "employees",
        "latest_deal_type",
        "financing_rounds",
        "investments",
        "description",
        "contact_information",
        "patents",
        "competitors",
        "research_analysis",
        "patent_activity",
        "all_investments",
        "faq",
        "investors",
    ],
}

VALIDATOR = Draft7Validator(SCHEMA)

def validate_records(records: Iterable[Dict[str, Any]]) -> List[str]:
    errors: List[str] = []
    for idx, record in enumerate(records):
        for error in VALIDATOR.iter_errors(record):
            msg = f"Record {idx}: {error.message}"
            errors.append(msg)
    if errors:
        LOGGER.debug("Schema validation produced %d error(s).", len(errors))
    return errors