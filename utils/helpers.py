# utils/helpers.py

import re
import logging

# Module- level logger
logger = logging.getLogger(__name__)

def format_filename(name):
    """
    # Convert a string into a safe filename

    # Steps:
    # 1. Lowercase everything
    # 2. Remove special characters
    # 3. Replace spaces with underscores

    # Example
    #"Artist live @ NYC!" -> "drake_live_nyc"
    """

    name = name.lower()
    
    # Remove anything that is not word, space, or dash
    name = re.sub(r'[^\w\s-]', '', name)

    # Replace spaces with underscores
    name = re.sub(r'\s+', '_', name.strip())

    return name


def make_json_safe(value):
    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except TypeError:
            pass

    if isinstance(value, dict):
        return {key: make_json_safe(item) for key, item in value.items()}

    if isinstance(value, list):
        return [make_json_safe(item) for item in value]

    return value


# In-memory cache for templates
_template_cache = {}


def load_template(path):
    """
    # Load a template file from disk caching

    # Behavior:
    # - First call -> reads file from disk
    # - Subsequent calls -> returns cached version

    # This avoids:
    # - repeated disk I/O
    # - unnecessary file reads (important in Streamlit reruns)
    """

    # Returned cached version if already loaded
    if path in _template_cache:
        return _template_cache[path]

    try:
        # Read template file
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()

            # Store in cache
            _template_cache[path] = content

            logger.info(f"Template loaded: {path}")
            
            return content

    except FileNotFoundError:
        logger.error(f"Template not found: {path}")
        raise

    except Exception as e:
        logger.exception(f"Unexpected error loading template: {path}")
        raise
