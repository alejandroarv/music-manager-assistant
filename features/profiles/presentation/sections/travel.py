# features/profiles/presentation/travel.py
# Streamlit UI framework

import streamlit as st


def render_terms_section(
    loaded_profile,
):
    """
    Render reusable travel and
    hospitality profile fields.

    Returns:
        dict
    """

    st.markdown(
        "### Travel & Hospitality"
    )

    air_transportation = st.text_input(
        "Air Transportation",

        value=(
            loaded_profile.air_transportation
            if loaded_profile
            else ""
        ),
    )

    hotel_accommodations = st.text_input(
        "Hotel Accommodations",

        value=(
            loaded_profile.hotel_accommodations
            if loaded_profile
            else ""
        ),
    )

    ground_transportation = st.text_input(
        "Ground Transportation",

        value=(
            loaded_profile.ground_transportation
            if loaded_profile
            else ""
        ),
    )

    meals_incidentals = st.text_input(
        "Meals & Incidentals",

        value=(
            loaded_profile.meals_incidentals
            if loaded_profile
            else ""
        ),
    )

    air_freight = st.selectbox(
        "Air Freight & Excess Baggage",

        options=[
            "Included",
            "Half Covered",
            "Not Included",
            "Custom",
        ],

        index=(
            [
                "Included",
                "Half Covered",
                "Not Included",
                "Custom",
            ].index(
                loaded_profile.air_freight
            )
            if (
                loaded_profile
                and loaded_profile.air_freight
                in [
                    "Included",
                    "Half Covered",
                    "Not Included",
                    "Custom",
                ]
            )
            else 2
        ),
    )

    return {

        "air_transportation": (
            air_transportation
        ),

        "hotel_accommodations": (
            hotel_accommodations
        ),

        "ground_transportation": (
            ground_transportation
        ),

        "meals_incidentals": (
            meals_incidentals
        ),

        "air_freight": (
            air_freight
        ),
    }