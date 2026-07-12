# features/companies/presentation/sections/identity.py

# Streamlit UI framework
import streamlit as st


def render_identity_section(
    loaded_profile,
):
    """
    Render company identity fields.

    Returns:
        dict
    """

    st.subheader(
        "Company Details"
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

    company_notes = st.text_area(

        "Company Notes",

        value=(

            loaded_profile.company_notes

            if loaded_profile

            else ""

        ),

    )

    return {

        "company_name": (
            company_name
        ),

        "company_address": (
            company_address
        ),

        "company_notes": (
            company_notes
        ),

    }