# core/models/company_profile.py

from dataclasses import (
    dataclass,
    field,
)


@dataclass
class CompanyProfile:
    """
    Represents a reusable company profile.

    Company profiles store business information
    that can automatically populate contracts
    and other workflows throughout the application.

    This model separates:
    - Company identity
    - Company contact information
    - Internal notes
    - Future expansion data
    """

    # Core company identity
    company_name: str

    # Company information
    company_address: str = ""

    # Internal notes
    company_notes: str = ""

    # Flexible storage for future expansion
    additional_data: dict = field(
        default_factory=dict,
    )

    def to_dict(self):
        """
        Convert the CompanyProfile into a dictionary.
        """

        return {

            "company_name": (
                self.company_name
            ),

            "company_address": (
                self.company_address
            ),

            "company_notes": (
                self.company_notes
            ),

            "additional_data": (
                self.additional_data
            ),

        }

    @classmethod
    def from_dict(
        cls,
        data,
    ):
        """
        Reconstruct a CompanyProfile
        from persisted data.
        """

        return cls(

            company_name=data.get(
                "company_name",
                "",
            ),

            company_address=data.get(
                "company_address",
                "",
            ),

            company_notes=data.get(
                "company_notes",
                "",
            ),

            additional_data=data.get(
                "additional_data",
                {},
            ),

        )