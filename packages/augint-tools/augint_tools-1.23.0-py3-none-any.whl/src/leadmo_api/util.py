import os
from aws_lambda_powertools import Logger

DEFAULT_ORIGIN = os.getenv("DEFAULT_ORIGIN", "https://localhost:5173")
APP_NAME = os.getenv("APP_NAME", "augint-tools")


def get_logger() -> Logger:
    log_level = os.environ.get("LOG_LEVEL", "INFO")  # Default to INFO if not set
    _logger = Logger(service=f"{APP_NAME}", level=log_level)
    return _logger


def get_headers(api_key: str, origin: str = DEFAULT_ORIGIN) -> dict:
    headers = {
        "Content-Type": "application/json",
        # "Origin": origin,
        "Authorization": f"Bearer {api_key}",
    }
    return headers


logger = get_logger()
