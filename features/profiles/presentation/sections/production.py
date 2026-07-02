# features/profiles/presentation/production.py
# Streamlit UI framework
import streamlit as st


def render_production_section(
    loaded_profile,
):
    """
    Render production-related
    profile defaults.

    Returns:
        dict
    """

    st.markdown(
        "### Production"
    )

    production = st.text_area(
        "Production",

        value=(
            loaded_profile.production
            if loaded_profile
            else ""
        ),
    )

    catering = st.text_area(
        "Catering",

        value=(
            loaded_profile.catering
            if loaded_profile
            else ""
        ),
    )

    special_provisions = st.text_area(
        "Special Provisions",

        value=(
            loaded_profile.special_provisions
            if loaded_profile
            else ""
        ),
    )

    return {

        "production": (
            production
        ),

        "catering": (
            catering
        ),

        "special_provisions": (
            special_provisions
        ),
    }