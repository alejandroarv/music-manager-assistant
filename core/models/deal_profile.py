# core/models/deal_profile.py

from dataclasses import (
    dataclass,
    asdict,
)


@dataclass
class DealProfile:
    """
    Reusable deal structure profile.

    Allows managers to save commonly-used
    booking deal structures.
    """

    profile_name: str = ""

    base_deal_type: str = (
        "Flat Guarantee"
    )

    flat_guarantee: float = 0.0

    percentage: float = 0.0

    deal_basis: str = "Net"

    minimum_guarantee: float = 0.0

    notes: str = ""

    def to_dict(
        self,
    ):
        return asdict(self)

    @classmethod
    def from_dict(
        cls,
        data,
    ):
        return cls(**data)