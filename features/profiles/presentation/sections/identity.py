# features/profiles/presentation/identity.py

# Streamlit UI framework
import streamlit as st


def render_identity_section(
    loaded_profile,
):
    """
    Render artist identity fields.

    Returns:
        dict
    """

    st.subheader(
        "Profile Details"
    )

    artist_name = st.text_input(
        "Artist Name",

        value=(
            loaded_profile.artist_name
            if loaded_profile
            else ""
        ),
    )

    company_name = st.text_input(
        "Company Name",

        value=(
            loaded_profile.company_name
            if loaded_profile
            else ""
        ),
    )

    company_address = st.text_area(
        "Company Address",

        value=(
            loaded_profile.company_address
            if loaded_profile
            else ""
        ),
    )

    return {

        "artist_name": artist_name,

        "company_name": company_name,

        "company_address": (
            company_address
        ),
    }