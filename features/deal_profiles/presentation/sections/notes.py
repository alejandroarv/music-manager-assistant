# features/deal_profiles/presentation/sections/notes.py

import streamlit as st


def render_notes_section(
    loaded_profile,
):
    """
    Render deal profile notes.
    """

    st.subheader(
        "Notes"
    )

    notes = st.text_area(

        "Notes",

        value=(

            loaded_profile.notes

            if loaded_profile

            else ""

        ),

    )

    return {

        "notes": notes,
    }