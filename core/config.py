# core/config.py

import os

# Base directory of the project (It's the root folder)
# It allows building paths dynamically no matter where the app is run from
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Settings:
    """
    # Centralized configuration for the entire app
    # Its purpose is to
    # - Store envirement-dependent values
    # - Avoid hardcoding paths and flags
    # - Make the app configurable without changing the code
    """

    # Path to storage file (JSON database)
    # Priority:
    # 1. Environment variable (allows dynamic configuration in different environments)
    # 2. Default path (data/storage.json in the project directory)
    STORAGE_FILE = os.getenv(
        "STORAGE_FILE",
        os.path.join(BASE_DIR, "data", "storage.json")
    )


    # Application name (used for display/logging if needed)
    APP_NAME = "Music Manager Assistant"

    # Debug flag (converted from string to boolean)
    # Example:
    # DEBUG=True -> True
    # DEBUG=False -> False
    DEBUG = os.getenv("DEBUG", "True") == "True"

# Singleton instance used accross the app
# Instead of importing Settings class we import this instance
settings = Settings()