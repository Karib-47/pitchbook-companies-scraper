from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Iterable, Mapping, Any

LOGGER = logging.getLogger(__name__)

def write_pretty_json(records: Iterable[Mapping[str, Any]], path: Path) -> None:
    data = list(records)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    LOGGER.info("Wrote pretty JSON with %d records to %s", len(data), path)

def write_jsonl(records: Iterable[Mapping[str, Any]], path: Path) -> None:
    count = 0
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
    LOGGER.info("Wrote JSONL with %d records to %s", count, path)