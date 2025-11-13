import argparse
import json
import logging
from pathlib import Path
from typing import List

from src.clients.pitchbook_client import PitchBookClient
from src.extractors.company_profile_parser import parse_company_profile
from src.extractors.investments_parser import parse_investments
from src.extractors.competitors_parser import parse_competitors
from src.extractors.faq_parser import parse_faq
from src.models.company_profile import CompanyProfile
from src.outputs.exporters import write_pretty_json, write_jsonl
from src.outputs.schema_validator import validate_records
from src.utils.http import HttpClient
from src.utils.logging_utils import setup_logging
from src.utils.rate_limiter import RateLimiter

LOGGER = logging.getLogger(__name__)

def load_settings(config_path: Path) -> dict:
    if not config_path.exists():
        LOGGER.warning("Settings file %s not found, using defaults.", config_path)
        return {
            "base_url": "https://pitchbook.com",
            "user_agent": "PitchbookCompanyProfileScraper/1.0 (+https://bitbash.dev)",
            "request_timeout": 15,
            "rate_limit_per_minute": 30,
            "output_dir": "data",
        }
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)

def load_inputs(input_path: Path) -> List[str]:
    if not input_path.exists():
        LOGGER.warning("Input file %s does not exist. No URLs to process.", input_path)
        return []
    urls: List[str] = []
    with input_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    return urls

def build_client(settings: dict) -> PitchBookClient:
    rate_limiter = RateLimiter(max_per_minute=settings.get("rate_limit_per_minute", 30))
    http_client = HttpClient(
        base_url=settings.get("base_url", "https://pitchbook.com"),
        user_agent=settings.get(
            "user_agent",
            "PitchbookCompanyProfileScraper/1.0 (+https://bitbash.dev)",
        ),
        timeout=settings.get("request_timeout", 15),
        rate_limiter=rate_limiter,
    )
    return PitchBookClient(http_client=http_client)

def process_url(client: PitchBookClient, url: str) -> dict:
    LOGGER.info("Processing %s", url)
    html = client.fetch_company_profile(url)
    basics = parse_company_profile(html, url)
    investments_summary, all_investments, investors = parse_investments(html)
    competitors = parse_competitors(html)
    faq = parse_faq(html)

    profile = CompanyProfile.from_parsed_parts(
        basics=basics,
        investments_summary=investments_summary,
        competitors=competitors,
        all_investments=all_investments,
        faq=faq,
        investors=investors,
    )
    record = profile.to_dict()
    LOGGER.debug("Built record for %s: %s", url, record)
    return record

def run(input_path: Path, output_path: Path, config_path: Path) -> None:
    setup_logging()
    LOGGER.info("Loading settings from %s", config_path)
    settings = load_settings(config_path)

    client = build_client(settings)
    urls = load_inputs(input_path)

    if not urls:
        LOGGER.warning("No URLs provided in %s. Nothing to do.", input_path)
        return

    records: List[dict] = []
    for url in urls:
        try:
            record = process_url(client, url)
            records.append(record)
        except Exception as exc:  # noqa: BLE001
            LOGGER.exception("Failed to process %s: %s", url, exc)

    errors = validate_records(records)
    if errors:
        LOGGER.warning("Schema validation completed with %d error(s).", len(errors))
        for err in errors:
            LOGGER.warning("Validation error: %s", err)
    else:
        LOGGER.info("All %d records validated successfully.", len(records))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_pretty_json(records, output_path)
    jsonl_path = output_path.with_suffix(".jsonl")
    write_jsonl(records, jsonl_path)

    LOGGER.info(
        "Finished. Wrote %d records to %s and %s",
        len(records),
        output_path,
        jsonl_path,
    )

def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    default_input = project_root / "data" / "inputs.sample.txt"
    default_output = project_root / "data" / "sample_output.json"
    default_config = project_root / "src" / "config" / "settings.example.json"

    parser = argparse.ArgumentParser(
        description="PitchBook Company Profile Scraper runner"
    )
    parser.add_argument(
        "--input",
        type=str,
        default=str(default_input),
        help="Path to input file containing PitchBook URLs, one per line.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(default_output),
        help="Path to output JSON file where records will be written.",
    )
    parser.add_argument(
        "--config",
        type=str,
        default=str(default_config),
        help="Path to JSON settings file.",
    )

    args = parser.parse_args()

    run(
        input_path=Path(args.input),
        output_path=Path(args.output),
        config_path=Path(args.config),
    )