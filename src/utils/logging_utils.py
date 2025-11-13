from __future__ import annotations

import logging
import logging.config
from pathlib import Path

def setup_logging(default_level: int = logging.INFO) -> None:
    """
    Configure logging using logging.conf if available, otherwise fall back to basicConfig.
    """
    here = Path(__file__).resolve()
    config_path = here.parents[1] / "config" / "logging.conf"

    if config_path.exists():
        try:
            logging.config.fileConfig(config_path, disable_existing_loggers=False)
            return
        except Exception:  # noqa: BLE001
            # Fallback to basic configuration on any error
            pass

    logging.basicConfig(level=default_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")