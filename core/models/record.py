# core/models/record.py

from dataclasses import asdict, dataclass
from typing import Any, Optional

@dataclass
class Record:
    """
    # Generic record model used for persistence

    # This is the universal structured stored in JSON
    # All features like booking, contracts, ect. are stored as records
    """

    # e.g, "booking", "contract"
    type: str
    # Human-readable identifier (e.g., artist name)
    name: str
    # Actual data payload (Like dict, string, etc.)
    content: dict
    # Extra searchable info
    metadata: Optional[dict] = None
    # Unique identifier
    id: Optional[str] = None
    # Creation time
    timestamp: Optional[str] = None

    def to_dict(self) -> dict:
        """
        # Convert record to dictionary for JSON storage
        """
        return asdict(self)
