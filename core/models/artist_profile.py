# core/models/artist_profile.py

from dataclasses import dataclass, field


@dataclass
class ArtistProfile:
    """
    Represts a reusable artist profile used throughout the application.

    Profiles store artist-specific information that can
    automatically populate future contracts and workflows

    This model separates:
    - Artist identity and preset relationships
    - Cached company snapshot data
    - Contract preset defaults
    - Flexible future expansion data
    """

    # Core artist identity
    artist_name: str

    # Reusable profile configuration name
    profile_name: str = "Default"

    # Cached company information copied
    # from the selected Default Company.
    # These values represent a snapshot
    # taken when the Artist Profile is
    # saved, allowing existing presets to
    # remain stable even if the Company
    # Profile changes later.
    company_name: str = ""
    company_address: str = ""

    # Default reusable company profile
    default_company: str = ""

    # Frequently reused contract clauses and provisions
    merchandising_terms: str = ""

# TODO:
# Verify with client whether this general
# concessionaire fee should remain or be
# replaced by the hard/soft merchandising
# concession structure.
    concessionaire_fee: str = ""

    seller: str = ""

    hard_merchandising: int = 100

    soft_merchandising: int = 100

    production: str = ""

    catering: str = ""

    special_provisions: str = ""

    # Transportation and hospitality requirements
    air_transportation: str = ""

    hotel_accommodations: str = ""

    ground_transportation: str = ""

    meals_incidentals: str = ""

    air_freight: str = "Not Included"

    # Default performance length for contracts
    show_length: str = "90 Minutes"

    # Default complimentary tickets preset
    complimentary_tickets: str = "None"

    # Internal notes for profile management
    profile_notes: str = ""

    # Default contract template associated with this artist
    default_contract_type: str = "performance"

    # Stores reusable contract field presets
    contract_defaults: dict = field(default_factory=dict)

    # Flexible storage for future expansion without needing schema changes
    additional_data: dict = field(default_factory=dict)

    def to_dict(self):
        """
        Converts the Artistprofile instance into a dictionary

        This is used when persisting profiles in the repository
        and JSON storage system
        """
        return {
            "artist_name": self.artist_name,
            "profile_name": self.profile_name,
            "company_name": self.company_name,
            "company_address": self.company_address,
            "default_company": self.default_company,
            "merchandising_terms": (
                self.merchandising_terms
            ),

            "concessionaire_fee": (
                self.concessionaire_fee
            ),

            "seller": (
                self.seller
            ),

            "hard_merchandising": (
                self.hard_merchandising
            ),

            "soft_merchandising": (
                self.soft_merchandising
            ),

            "production": (
                self.production
            ),
            
            "catering": self.catering,
            "special_provisions": self.special_provisions,
            "air_transportation": self.air_transportation,
            "hotel_accommodations": self.hotel_accommodations,
            "ground_transportation": (
                self.ground_transportation
            ),

            "meals_incidentals": (
                self.meals_incidentals
            ),

            "air_freight": (
                self.air_freight
            ),

            "show_length": self.show_length,
            "complimentary_tickets": (
                self.complimentary_tickets
            ),
            "profile_notes": self.profile_notes,
            "default_contract_type": self.default_contract_type,
            "contract_defaults": self.contract_defaults,
            "additional_data": self.additional_data,
        }
    
    @staticmethod
    def normalize_percentage(
        value,
    ):
        """
        Normalize legacy merchandising values.

        Older profiles stored values such as:
        - Allowed
        - Restricted
        - Not Allowed

        New profiles store integer percentages.
        """

        if isinstance(
            value,
            int,
        ):

            return value

        try:

            return int(value)

        except (
            TypeError,
            ValueError,
        ):

            return 100
        
    @classmethod
    def from_dict(cls, data):
        """
        Reconstructs in ArtistProfile object from a dictionary

        This allows profile records retrieved from storage to be converted
        back into strongly-typed model objects
        """
        
        return cls(
            artist_name=data.get("artist_name", ""),
            profile_name=data.get(
                "profile_name",
                "Default",
            ),
            company_name=data.get("company_name", ""),
            company_address=data.get("company_address", ""),
            default_company=data.get(
                "default_company",
                "",
            ),
            merchandising_terms=data.get(
                "merchandising_terms",
                "",
            ),

            concessionaire_fee=data.get(
                "concessionaire_fee",
                "",
            ),

            seller=data.get(
                "seller",
                "",
            ),

            hard_merchandising=(
                cls.normalize_percentage(

                    data.get(
                        "hard_merchandising",
                        100,
                    )

                )
            ),

            soft_merchandising=(
                cls.normalize_percentage(

                    data.get(
                        "soft_merchandising",
                        100,
                    )

                )
            ),

            production=data.get(
                "production",
                ""
            ),
            catering=data.get(
                "catering",
                ""
            ),
            special_provisions=data.get("special_provisions", ""),
            air_transportation=data.get("air_transportation", ""),
            hotel_accommodations=data.get("hotel_accommodations", ""),
            ground_transportation=data.get(
                "ground_transportation",
                "",
            ),

            meals_incidentals=data.get(
                "meals_incidentals",
                "",
            ),

            air_freight=data.get(
                "air_freight",
                "Not Included",
            ),

            show_length=data.get(
                "show_length",
                "90 Minutes",
            ),
            complimentary_tickets=data.get(
                "complimentary_tickets",
                "",
            ),
            profile_notes=data.get("profile_notes", ""),
            default_contract_type=data.get(
                "default_contract_type",
                "performance",
            ),
            contract_defaults=data.get(
                "contract_defaults",
                {},
            ),
            additional_data=data.get(
                "additional_data",
                {},
            ),
        )