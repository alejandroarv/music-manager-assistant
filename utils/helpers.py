# utils/helpers.py

import logging
import re


# Module-level logger used for helper
# and utility-related operations
logger = logging.getLogger(__name__)


def format_filename(name):
    """
    Convert arbitrary text into a safe,
    filesystem-friendly filename.

    Processing steps:
    - Convert to lowercase
    - Remove special characters
    - Replace spaces with underscores

    Example:
        "Artist live @ NYC!"
        ->
        "artist_live_nyc"
    """

    # Normalize casing
    name = name.lower()

    # Remove unsupported filename characters
    name = re.sub(
        r"[^\w\s-]",
        "",
        name,
    )

    # Normalize whitespace into underscores
    name = re.sub(
        r"\s+",
        "_",
        name.strip(),
    )

    return name


def make_json_safe(value):
    """
    Recursively convert values into
    JSON-serializable structures.

    Handles:
    - datetime/date objects
    - nested dictionaries
    - nested lists

    Returns:
        JSON-safe normalized value.
    """

    # Convert datetime-like objects
    # using ISO formatting
    if hasattr(value, "isoformat"):

        try:

            return value.isoformat()

        except TypeError:

            pass

    # Recursively normalize dictionaries
    if isinstance(value, dict):

        return {
            key: make_json_safe(item)
            for key, item in value.items()
        }

    # Recursively normalize lists
    if isinstance(value, list):

        return [
            make_json_safe(item)
            for item in value
        ]

    return value


# In-memory cache for reusable template content
_template_cache = {}


def load_template(path):
    """
    Load and cache text-based templates.

    Behavior:
    - First load reads from disk
    - Subsequent loads use in-memory cache

    Benefits:
    - Reduces repeated disk I/O
    - Improves Streamlit rerun performance
    - Avoids unnecessary file reads
    """

    # Return cached template when available
    if path in _template_cache:

        return _template_cache[path]

    try:

        # Read template file contents
        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

            # Store template in cache
            _template_cache[path] = content

            logger.info(
                f"Template loaded: {path}"
            )

            return content

    except FileNotFoundError:

        logger.error(
            f"Template not found: {path}"
        )

        raise

    except Exception:

        logger.exception(
            "Unexpected error loading "
            f"template: {path}"
        )

        raise

def format_fee_input(session_state, key):
    """
    Auto-format fee input with commas.
    """

    raw_value = (
        session_state[key]
        .replace(",", "")
        .strip()
    )

    # Ignore invalid input
    if not raw_value.isdigit():
        return

    session_state[key] = (
        f"{int(raw_value):,}"
    )