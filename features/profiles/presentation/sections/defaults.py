# features/profiles/presentation/defaults.py

# Streamlit UI framework
import streamlit as st


def render_defaults_section(
    loaded_profile,
):
    """
    Render default performance
    profile values.

    Returns:
        dict
    """

    st.markdown(
        "### Performance Defaults"
    )

    show_length = st.text_input(
        "Default Show Length",

        value=(
            loaded_profile.show_length
            if loaded_profile
            else "90 Minutes"
        ),
    )

    return {

        "show_length": (
            show_length
        ),
    }