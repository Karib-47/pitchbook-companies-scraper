from __future__ import annotations

import json
from pathlib import Path

from src.outputs.schema_validator import validate_records

def test_sample_output_conforms_to_schema():
    project_root = Path(__file__).resolve().parents[1]
    sample_path = project_root / "data" / "sample_output.json"
    assert sample_path.exists(), f"Sample output file not found at {sample_path}"

    with sample_path.open("r", encoding="utf-8") as f:
        records = json.load(f)

    errors = validate_records(records)
    assert errors == []