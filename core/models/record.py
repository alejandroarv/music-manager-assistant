# core/models/record.py

from dataclasses import asdict, dataclass
from typing import Any, Optional

@dataclass
class Record:
    """
    Generic persistence model used across the application

    Records represent the standardized structure stored in 
    JSON persistence regardless of feature type

    Examples:
    - Bookings
    - Contracts
    - Tour entries
    - Historical records

    This model acts as a shared persistence wrapper that allows different
    features to store structured data in a consistent format
    """

    # Record category identifier
    type: str

    # Human-readable display name
    name: str

    # Primary structured payload associated with the record
    content: dict

    # Optional searchable or filtering metadata
    metadata: Optional[dict] = None

    # Unique record identifier
    id: Optional[str] = None

    # Record creation timestamp
    timestamp: Optional[str] = None

    def to_dict(self) -> dict:
        """
        Convert the record into a serializable dictionary 
        for JSON persistence
        """
        return asdict(self)
