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

        return {

            # Artist / company information
            "artist_name": profile.artist_name,

            "company_name": profile.company_name,

            "company_address": (
                profile.company_address
            ),

            # Purchaser information
            "purchaser_name": (
                profile.purchaser_name
            ),

            "purchaser_address": (
                profile.purchaser_address
            ),

            # Contract signatory
            "signatory": profile.signatory,

            # Reusable contract clauses
            "merchandising_terms": (
                profile.merchandising_terms
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

            # Show defaults
            "show_length": (
                profile.show_length
            ),

            # Contract preset defaults
            "contract_defaults": (
                profile.contract_defaults
            ),
        }