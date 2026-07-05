# features/venue_profiles/application/service.py

# Record type constant used for venue profile persistence
from core.constants import VENUE_PROFILE

# Strongly-typed venue profile model
from core.models.venue_profile import (
    VenueProfile,
)

# Generic persistence record model
from core.models.record import Record


class VenueProfileService:
    """
    Application service responsible for
    venue profile operations.

    Responsibilities:
    - create venue profiles
    - retrieve venue profiles
    - update venue profiles
    - delete venue profiles
    """

    def __init__(
        self,
        record_repository,
    ):

        self.record_repository = (
            record_repository
        )

    def create_profile(
        self,
        profile: VenueProfile,
    ):
        """
        Persist a venue profile.
        """

        record = Record(

            type=VENUE_PROFILE,

            name=profile.venue_name,

            content=profile.to_dict(),

            metadata={
                "venue": profile.venue_name,
            },
        )

        self.record_repository.save(
            record
        )

        return record

    def get_all_profiles(
        self,
    ):
        """
        Retrieve all saved venue profiles.
        """

        records = (
            self.record_repository
            .get_by_type(
                VENUE_PROFILE
            )
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

    def get_profile_by_venue(
        self,
        venue_name,
    ):
        """
        Retrieve a venue profile
        by venue name.
        """

        profiles = (
            self.record_repository
            .get_by_type(
                VENUE_PROFILE
            )
        )

        for record in profiles:

            if (

                record.get(
                    "name",
                    ""
                ).strip().lower()

                ==

                venue_name.strip().lower()

            ):

                return VenueProfile.from_dict(
                    record.get(
                        "content",
                        {},
                    )
                )

        return None

    def delete_profile(
        self,
        record_id,
    ):
        """
        Delete a venue profile.
        """

        self.record_repository.delete(
            record_id
        )

    def update_profile(
        self,
        record_id,
        updated_profile,
    ):
        """
        Update an existing venue profile.
        """

        self.delete_profile(
            record_id
        )

        return self.create_profile(
            updated_profile
        )
    
    def create_profile_from_contract(
        self,
        form_data,
    ):
        """
        Create or update a venue profile
        from performance contract data.
        """

        shows = form_data.get(
            "shows",
            [],
        )

        venue_capacity = (
            shows[0].get(
                "capacity",
                "",
            )
            if shows
            else ""
        )

        profile = VenueProfile(

            venue_name=form_data.get(
                "venue",
                "",
            ),

            city=form_data.get(
                "city",
                "",
            ),

            venue_address=form_data.get(
                "venue_address",
                "",
            ),

            venue_capacity=venue_capacity,
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
                    profile.venue_name.strip().lower()
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
