"""
Logging setup for MythCode with credential redaction.
"""
import logging
import re
import sys

class RedactingFormatter(logging.Formatter):
    """Redacts potential API keys or sensitive tokens from logs."""
    KEY_PATTERN = re.compile(r'(api[-_]?key|token|secret|authorization)[:=]\s*["\']?([^"\'\s]+)["\']?', re.IGNORECASE)

    def format(self, record: logging.LogRecord) -> str:
        original = super().format(record)
        return self.KEY_PATTERN.sub(r'\1: [REDACTED]', original)

def setup_logger(name: str = "MythCode") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            RedactingFormatter("[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s")
        )
        logger.addHandler(handler)
    return logger
