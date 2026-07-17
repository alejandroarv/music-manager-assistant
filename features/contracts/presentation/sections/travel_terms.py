# features/contracts/presentation/sections/travel_terms.py

# Streamlit UI framework
import streamlit as st


def render_terms_section(
    key_prefix,
):
    """
    Render travel, hospitality,
    and reusable contract clause fields.

    Responsibilities:
    - render logistics inputs
    - render reusable terms inputs
    - collect normalized section data

    Returns:
        dict: Normalized section values
    """


    # Terms Section Header
    st.markdown("### Terms")

    col8, col9 = st.columns(2)


    # Travel & Logistics Fields
    with col8:

        air_transportation = st.text_input(
            "Air Transportation",
            key=f"{key_prefix}_air_transportation",
        )

        hotel_accommodations = st.text_input(
            "Hotel Accommodations",
            key=f"{key_prefix}_hotel_accommodations",
        )

        air_freight = st.text_input(
            "Air Freight & Excess Baggage",
            key=f"{key_prefix}_air_freight",
        )

        ground_transportation = st.text_input(
            "Ground Transportation",
            key=f"{key_prefix}_ground_transportation",
        )

        meals_incidentals = st.text_input(
            "Meals & Incidentals",
            key=f"{key_prefix}_meals_incidentals",
        )

        visas_required = st.selectbox(
            "Visas Required",
            ["Yes", "No"],
            key=f"{key_prefix}_visas_required",
        )
        
        visa_responsible_party = st.selectbox(
            "Visa Responsible Party",
            ["Purchaser", "Company"],
            key=f"{key_prefix}_visa_responsible_party",
        )
    # Business & Contract Fields
    with col9:

        # Merchandising
        st.markdown(
            "#### Merchandising"
        )

        concessionaire_fee = st.text_input(
            "Concessionaire Fee",
            key=f"{key_prefix}_concessionaire_fee",
        )

        seller = st.text_input(
            "Seller",
            key=f"{key_prefix}_seller",
        )

        complimentary_tickets = st.text_input(
            "Complimentary Tickets",
            key=f"{key_prefix}_complimentary_tickets",
        )

        # Production
        st.markdown(
            "#### Production"
        )

        production = st.text_area(
            "Production",
            key=f"{key_prefix}_production",
        )

        catering = st.text_area(
            "Catering",
            key=f"{key_prefix}_catering",
        )

        special_provisions = st.text_area(
            "Special Provisions",
            key=f"{key_prefix}_special_provisions",
        )

    # Return normalized section payload
    return {
        "air_transportation": (
            air_transportation
        ),

        "hotel_accommodations": (
            hotel_accommodations
        ),

        "air_freight": (
            air_freight
        ),

        "ground_transportation": (
            ground_transportation
        ),

        "meals_incidentals": (
            meals_incidentals
        ),

        "visas_required": (
            visas_required == "Yes"
        ),

        "visa_responsible_party": (
            visa_responsible_party
        ),

        "complimentary_tickets": (
            complimentary_tickets
        ),

        "concessionaire_fee": (
            concessionaire_fee
        ),

        "seller": (
            seller
        ),

        "special_provisions": (
            special_provisions
        ),

        "production": (
            production
        ),

        "catering": (
            catering
        ),
    }