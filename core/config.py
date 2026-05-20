# core/config.py

import os


# Root directory of the application.
# Used to construct absolute project paths dynamically.
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


class Settings:
    """
    Centralized application configuration.

    Responsibilities:
    - Store environment-dependent settings
    - Centralize configurable application values
    - Avoid hardcoded paths and flags
    - Support environment-based deployment configuration
    """

    # Path to the persistence storage file.
    # Priority:
    # 1. Environment variable override
    # 2. Default local project storage path
    STORAGE_FILE = os.getenv(
        "STORAGE_FILE",
        os.path.join(
            BASE_DIR,
            "data",
            "storage.json"
        )
    )

    # Application display name
    APP_NAME = "Music Manager Assistant"

    # Debug mode flag
    DEBUG = os.getenv(
        "DEBUG",
        "True"
    ) == "True"


# Shared configuration instance used throughout the app
settings = Settings()