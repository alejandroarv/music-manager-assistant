# features/deal_profiles/application/service.py

from core.models.deal_profile import (
    DealProfile,
)

from core.models.record import (
    Record,
)

from core.repositories.interface import (
    Repository,
)


class DealProfileService:
    """
    Service responsible for managing
    reusable deal structure profiles.
    """

    def __init__(
        self,
        repository: Repository,
    ):
        self.repo = repository

    def get_profiles(
        self,
    ) -> list[dict]:

        return self.repo.get_by_type(
            "deal_profile"
        )

    def save_profile(
        self,
        profile: DealProfile,
        record_id=None,
    ):

        record = Record(

            id=record_id,

            type="deal_profile",

            name=profile.profile_name,

            content=profile.to_dict(),

        )

        if record_id:

            self.repo.update(
                record
            )

        else:

            self.repo.save(
                record
            )
            
    def delete_profile(
        self,
        record_id: str,
    ):

        self.repo.delete(
            record_id
        )