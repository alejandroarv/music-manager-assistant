# core/templates.py

from docx import Document
import os
from core.config import BASE_DIR
from utils.helpers import load_template

TEMPLATES = {
    "performance_single": os.path.join(BASE_DIR, "templates", "performance_single.docx"),
    "performance_multi": os.path.join(BASE_DIR, "templates", "performance_multi.docx"),
    "nda": os.path.join(BASE_DIR, "templates", "nda.txt"),
}

def get_template(template_name: str):
    if template_name not in TEMPLATES:
        raise ValueError(f"Unknown template: {template_name}")

    path = TEMPLATES[template_name]
    _, extension = os.path.splitext(path)

    if extension.lower() == ".docx":
        return Document(path)

    return load_template(path)
