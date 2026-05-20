# core/templates.py

import os

from docx import Document

from core.config import BASE_DIR
from utils.helpers import load_template


# Centralized template registry used for document generation
TEMPLATES = {
    "performance_single": os.path.join(
        BASE_DIR,
        "templates",
        "performance_single.docx"
    ),

    "performance_multi": os.path.join(
        BASE_DIR,
        "templates",
        "performance_multi.docx"
    ),

    "nda": os.path.join(
        BASE_DIR,
        "templates",
        "nda.txt"
    ),
}


def get_template(template_name: str):
    """
    Load and return a template resource by name.

    Supports:
    - DOCX document templates
    - Plain text templates

    Args:
        template_name: Registered template identifier.

    Returns:
        Loaded template object or text content.

    Raises:
        ValueError: If the template name is unknown.
    """

    if template_name not in TEMPLATES:
        raise ValueError(
            f"Unknown template: {template_name}"
        )

    path = TEMPLATES[template_name]
    _, extension = os.path.splitext(path)

    # Load DOCX templates as editable document objects
    if extension.lower() == ".docx":
        return Document(path)

    # Load text-based templates as raw content
    return load_template(path)
