import logging
import sys
from logging.handlers import RotatingFileHandler


def setup_logging():
    """Configure application logging with rotation and UTF-8 support."""

    console_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler(
        "ai_comment_service.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB per file
        backupCount=5,  # keep up to 5 old files
        encoding="utf-8",
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[console_handler, file_handler],
    )

    # Fix console encoding for Windows
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
