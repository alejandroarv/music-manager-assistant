# features/deal_profiles/presentation/sections/general.py

# Streamlit UI framework
import streamlit as st

from core.constants import (
    DEAL_TYPES,
)

def render_general_section(
    loaded_profile,
):
    """
    Render general deal profile information.
    """

    st.subheader(
        "General"
    )

    profile_name = st.text_input(

        "Profile Name",

        value=(

            loaded_profile.profile_name

            if loaded_profile

            else ""

        ),

    )

    base_deal_type = st.selectbox(

        "Base Deal",

        options=DEAL_TYPES,

        index=(

            DEAL_TYPES.index(

                loaded_profile.base_deal_type

            )

            if loaded_profile

            else 0

        ),

    )

    return {

        "profile_name": (
            profile_name
        ),

        "base_deal_type": (
            base_deal_type
        ),

    }