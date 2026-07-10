# features/profiles/domain/logic.py

"""
Pure business logic for Artist Profiles.

Responsibilities:
- Build profile models
- Normalize profile data
- Validate profile rules
- Prepare profile payloads

This module must remain independent from:
- Streamlit
- Repositories
- JSON storage
- Session State
"""


from core.models.artist_profile import (
    ArtistProfile,
)


def build_artist_profile(
    **profile_data,
):
    """
    Build a normalized ArtistProfile instance.

    This keeps profile construction out of
    the presentation layer and allows future
    normalization and validation to happen
    in one place.
    """

    return ArtistProfile(
        **profile_data,
    )