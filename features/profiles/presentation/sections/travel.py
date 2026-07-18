# features/profiles/presentation/travel.py
# Streamlit UI framework

import streamlit as st

from features.contracts.presentation.sections.travel_terms import (
    AIR_FREIGHT_YES_DEFAULT,
    AIR_TRANSPORTATION_YES_DEFAULT,
    GROUND_TRANSPORTATION_YES_DEFAULT,
    HOTEL_ACCOMMODATIONS_YES_DEFAULT,
    MEALS_INCIDENTALS_YES_DEFAULT,
)


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
            else AIR_TRANSPORTATION_YES_DEFAULT
        ),
    )

    hotel_accommodations = st.text_input(
        "Hotel Accommodations",

        value=(
            loaded_profile.hotel_accommodations
            if loaded_profile
            else HOTEL_ACCOMMODATIONS_YES_DEFAULT
        ),
    )

    ground_transportation = st.text_input(
        "Ground Transportation",

        value=(
            loaded_profile.ground_transportation
            if loaded_profile
            else GROUND_TRANSPORTATION_YES_DEFAULT
        ),
    )

    meals_incidentals = st.text_input(
        "Meals & Incidentals",

        value=(
            loaded_profile.meals_incidentals
            if loaded_profile
            else MEALS_INCIDENTALS_YES_DEFAULT
        ),
    )

    air_freight = st.text_input(
        "Air Freight & Excess Baggage",

        value=(
            loaded_profile.air_freight
            if loaded_profile
            else AIR_FREIGHT_YES_DEFAULT
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
