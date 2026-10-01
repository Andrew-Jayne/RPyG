import logging
from datetime import datetime
from pathlib import Path

from RPyG.utilities import ensure_type


DEFAULT_PATH = Path("./logs")


def setup_logging(log_level: int = logging.INFO, log_dir: Path = DEFAULT_PATH) -> Path:
    ensure_type(log_level, int, "log_level")
    ensure_type(log_dir, Path, "log_dir")
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"log-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        # 2026-10-01 09:13:08,049 [INFO] RPyG.launch: opening new log file at logs/log-20261001-091308.log
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
        force=True,  # replaces any handlers already on the root logger
    )
    return log_file
