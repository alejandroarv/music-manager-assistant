# features/profiles/application/service.py

# Record type constant used for profile persistence
from core.constants import ARTIST_PROFILE

# Strongly-typed domain model for artist profiles
from core.models.artist_profile import ArtistProfile

# Generic persistence record model used throughout the app
from core.models.record import Record


class ProfileService:
    """
    Application service responsible for managing
    artist profile operations.

    Responsibilities:
    - create profiles
    - retrieve profiles
    - delete profiles
    - convert storage records into domain models
    """

    def __init__(self, record_repository):
        """
        Inject shared repository dependency.
        """

        self.record_repository = record_repository

    def create_profile(self, profile: ArtistProfile):
        """
        Persist a new artist profile.
        """

        # Convert the profile model into a generic record
        record = Record(
            type=ARTIST_PROFILE,

            # Human-readable display name
            name=profile.artist_name,

            # Serialized profile data
            content=profile.to_dict(),

            # Lightweight searchable metadata
            metadata={
                "artist": profile.artist_name,
            },
        )

        # Save the record using the shared repository
        self.record_repository.save(record)

        return record

    def get_all_profiles(self):
        """
        Retrieve all saved artist profiles.

        Converts raw repository dictionaries into
        lightweight profile summary objects.

        Returns:
            list[dict]
        """

        records = self.record_repository.get_by_type(
            ARTIST_PROFILE
        )

        profiles = []

        for record in records:

            profiles.append({
                "id": record.get("id"),

                "name": record.get("name"),

                "content": record.get(
                    "content",
                    {},
                ),

                "metadata": record.get(
                    "metadata",
                    {},
                ),

                "timestamp": record.get(
                    "timestamp"
                ),
            })

        return profiles
    
    def get_profile_by_artist(
        self,
        artist_name,
    ):
        """
        Retrieve a single profile by artist name.

        Returns:
            ArtistProfile | None
        """

        profiles = (
            self.record_repository.get_by_type(
                ARTIST_PROFILE
            )
        )

        for record in profiles:

            # Compare normalized artist names
            if (
                record.get(
                    "name",
                    ""
                ).strip().lower()
                ==
                artist_name.strip().lower()
            ):

                # Convert stored profile content
                # into a strongly-typed model
                return ArtistProfile.from_dict(
                    record.get(
                        "content",
                        {}
                    )
                )

        return None

    def delete_profile(self, record_id):
        """
        Delete an artist profile by record ID.
        """

        self.record_repository.delete(
            record_id
        )
    
    def update_profile(
        self,
        record_id,
        updated_profile: ArtistProfile,
    ):
        """
        Update an existing artist profile.

        Current implementation:
        - deletes old record
        - creates new updated record

        This approach keeps the repository
        layer simple for now.
        """

        # Remove old profile record
        self.delete_profile(record_id)

        # Save updated profile
        return self.create_profile(
            updated_profile
        )   
    
    def build_form_defaults(
        self,
        profile: ArtistProfile,
    ):
        """
        Convert a profile into reusable
        contract form default values.

        This keeps autofill mapping logic
        centralized inside the service layer
        rather than spreading it across UI code.
        """

        contract_defaults = (
            profile.contract_defaults
            or {}
        )

        return {

            # Artist / company information
            "artist_name": profile.artist_name,

            "company_name": profile.company_name,

            "company_address": (
                profile.company_address
            ),

            # Reusable contract clauses
            "merchandising_terms": (
                profile.merchandising_terms
            ),

            "concessionaire_fee": (
                profile.concessionaire_fee
            ),

            "seller": (
                profile.seller
            ),

            "hard_merchandising": (
                profile.hard_merchandising
            ),

            "soft_merchandising": (
                profile.soft_merchandising
            ),

            "production": (
                profile.production
            ),

            "catering": (
                profile.catering
            ),

            "special_provisions": (
                profile.special_provisions
            ),

            # Transportation / hospitality
            "air_transportation": (
                profile.air_transportation
            ),

            "hotel_accommodations": (
                profile.hotel_accommodations
            ),

            "ground_transportation": (
                profile.ground_transportation
            ),

            "meals_incidentals": (
                profile.meals_incidentals
            ),

            "air_freight": (
                profile.air_freight
            ),
            
            # Show defaults
            "show_length": (
                profile.show_length
            ),

            "capacity": (
                contract_defaults.get(
                    "capacity",
                    "",
                )
            ),

            "notes": (
                contract_defaults.get(
                    "notes",
                    "",
                )
            ),

            "complimentary_tickets": (
                profile.complimentary_tickets
            ),

            # Contract preset defaults
            "contract_defaults": (
                contract_defaults
            ),
        }
    
    def save_profile_from_contract(
        self,
        form_data,
    ):
        """
        Create an artist profile from
        performance contract form data.
        """

        profile = ArtistProfile(

            artist_name=form_data.get(
                "artist",
                "",
            ),

            company_name=form_data.get(
                "company_name",
                "",
            ),

            company_address=form_data.get(
                "company_address",
                "",
            ),

            air_transportation=form_data.get(
                "air_transportation",
                "",
            ),

            hotel_accommodations=form_data.get(
                "hotel_accommodations",
                "",
            ),

            ground_transportation=form_data.get(
                "ground_transportation",
                "",
            ),

            meals_incidentals=form_data.get(
                "meals_incidentals",
                "",
            ),

            air_freight=form_data.get(
                "air_freight",
                "",
            ),

            show_length=form_data.get(
                "show_length",
                "90 Minutes",
            ),

            complimentary_tickets=form_data.get(
                "complimentary_tickets",
                "",
            ),

            merchandising_terms=form_data.get(
                "merchandising_terms",
                "",
            ),

            concessionaire_fee=form_data.get(
                "concessionaire_fee",
                "",
            ),

            seller=form_data.get(
                "seller",
                "",
            ),

            hard_merchandising=form_data.get(
                "hard_merchandising",
                "",
            ),

            soft_merchandising=form_data.get(
                "soft_merchandising",
                "",
            ),

            production=form_data.get(
                "production",
                "",
            ),

            catering=form_data.get(
                "catering",
                "",
            ),

            special_provisions=form_data.get(
                "special_provisions",
                "",
            ),

            contract_defaults={
                # Reusable show defaults
                # captured from contracts
                "capacity": form_data.get(
                    "capacity",
                    "",
                ),

                "notes": form_data.get(
                    "notes",
                    "",
                ),
            },
        )

        existing_profiles = (
            self.get_all_profiles()
        )

        existing_record = next(
            (
                record
                for record in existing_profiles
                if (
                    record["name"].strip().lower()
                    ==
                    profile.artist_name.strip().lower()
                )
            ),
            None,
        )

        if existing_record:

            return self.update_profile(
                existing_record["id"],
                profile,
            )

        return self.create_profile(
            profile
        )
