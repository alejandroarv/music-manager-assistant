# core/models/venue_profile.py

from dataclasses import dataclass


@dataclass
class VenueProfile:
    """
    Represents a reusable venue profile.

    Venue profiles store location-specific
    information that can automatically
    populate future contracts.
    """

    venue_name: str

    city: str = ""

    venue_address: str = ""

    venue_capacity: str = ""

    venue_notes: str = ""

    def to_dict(self):

        return {

            "venue_name": self.venue_name,

            "city": self.city,

            "venue_address": self.venue_address,

            "venue_capacity": self.venue_capacity,

            "venue_notes": self.venue_notes,
        }

    @classmethod
    def from_dict(
        cls,
        data,
    ):

        return cls(

            venue_name=data.get(
                "venue_name",
                "",
            ),

            city=data.get(
                "city",
                "",
            ),

            venue_address=data.get(
                "venue_address",
                "",
            ),

            venue_capacity=data.get(
                "venue_capacity",
                "",
            ),

            venue_notes=data.get(
                "venue_notes",
                "",
            ),
        )