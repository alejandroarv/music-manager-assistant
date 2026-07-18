# features/contracts/presentation/sections/travel_terms.py

# Streamlit UI framework
import streamlit as st


AIR_TRANSPORTATION_YES_DEFAULT = (
    "Purchaser shall provide and pay for round-trip economy airfare "
    "for Artist and Artist's approved touring personnel."
)

AIR_TRANSPORTATION_NO_DEFAULT = (
    "Artist shall be responsible for all air transportation arrangements "
    "and expenses unless otherwise agreed in writing."
)

HOTEL_ACCOMMODATIONS_YES_DEFAULT = (
    "Purchaser shall provide hotel accommodations consisting of the agreed "
    "number of single and double occupancy rooms at a minimum three-star "
    "hotel, unless otherwise agreed in writing."
)

HOTEL_ACCOMMODATIONS_NO_DEFAULT = (
    "Artist shall be responsible for securing and paying for all hotel "
    "accommodations unless otherwise agreed in writing."
)

GROUND_TRANSPORTATION_YES_DEFAULT = (
    "Purchaser shall provide all required local ground transportation "
    "between the airport, hotel, venue, and any approved promotional "
    "appearances."
)

GROUND_TRANSPORTATION_NO_DEFAULT = (
    "Artist shall be responsible for all local ground transportation "
    "arrangements and expenses unless otherwise agreed in writing."
)

MEALS_INCIDENTALS_YES_DEFAULT = (
    "Purchaser shall provide reasonable meals and incidental expenses "
    "for Artist and Artist's approved touring personnel throughout the "
    "engagement."
)

MEALS_INCIDENTALS_NO_DEFAULT = (
    "Artist shall be responsible for all meals and incidental expenses "
    "unless otherwise agreed in writing."
)

AIR_FREIGHT_YES_DEFAULT = (
    "Purchaser shall reimburse all approved air freight and excess baggage "
    "charges reasonably incurred in connection with the performance."
)

AIR_FREIGHT_NO_DEFAULT = (
    "Artist shall be responsible for all air freight and excess baggage "
    "charges unless otherwise agreed in writing."
)


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

        air_transportation_required = st.selectbox(
            "Air Transportation",
            ["Yes", "No"],
            key=f"{key_prefix}_air_transportation_required",
        )

        air_transportation_yes = st.text_input(
            "If Yes",
            value=AIR_TRANSPORTATION_YES_DEFAULT,
            key=f"{key_prefix}_air_transportation_yes",
        )

        air_transportation_no = st.text_input(
            "If No",
            value=AIR_TRANSPORTATION_NO_DEFAULT,
            key=f"{key_prefix}_air_transportation_no",
        )

        hotel_accommodations_required = st.selectbox(
            "Hotel Accommodations",
            ["Yes", "No"],
            key=f"{key_prefix}_hotel_accommodations_required",
        )

        hotel_accommodations_yes = st.text_input(
            "If Yes",
            value=HOTEL_ACCOMMODATIONS_YES_DEFAULT,
            key=f"{key_prefix}_hotel_accommodations_yes",
        )

        hotel_accommodations_no = st.text_input(
            "If No",
            value=HOTEL_ACCOMMODATIONS_NO_DEFAULT,
            key=f"{key_prefix}_hotel_accommodations_no",
        )

        air_freight_required = st.selectbox(
            "Air Freight & Excess Baggage",
            ["Yes", "No"],
            key=f"{key_prefix}_air_freight_required",
        )

        air_freight_yes = st.text_input(
            "If Yes",
            value=AIR_FREIGHT_YES_DEFAULT,
            key=f"{key_prefix}_air_freight_yes",
        )

        air_freight_no = st.text_input(
            "If No",
            value=AIR_FREIGHT_NO_DEFAULT,
            key=f"{key_prefix}_air_freight_no",
        )

        ground_transportation_required = st.selectbox(
            "Ground Transportation",
            ["Yes", "No"],
            key=f"{key_prefix}_ground_transportation_required",
        )

        ground_transportation_yes = st.text_input(
            "If Yes",
            value=GROUND_TRANSPORTATION_YES_DEFAULT,
            key=f"{key_prefix}_ground_transportation_yes",
        )

        ground_transportation_no = st.text_input(
            "If No",
            value=GROUND_TRANSPORTATION_NO_DEFAULT,
            key=f"{key_prefix}_ground_transportation_no",
        )

        meals_incidentals_required = st.selectbox(
            "Meals & Incidentals",
            ["Yes", "No"],
            key=f"{key_prefix}_meals_incidentals_required",
        )

        meals_incidentals_yes = st.text_input(
            "If Yes",
            value=MEALS_INCIDENTALS_YES_DEFAULT,
            key=f"{key_prefix}_meals_incidentals_yes",
        )

        meals_incidentals_no = st.text_input(
            "If No",
            value=MEALS_INCIDENTALS_NO_DEFAULT,
            key=f"{key_prefix}_meals_incidentals_no",
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
        "air_transportation_required": (
            air_transportation_required == "Yes"
        ),

        "air_transportation_yes": (
            air_transportation_yes
        ),

        "air_transportation_no": (
            air_transportation_no
        ),

        "hotel_accommodations_required": (
            hotel_accommodations_required == "Yes"
        ),

        "hotel_accommodations_yes": (
            hotel_accommodations_yes
        ),

        "hotel_accommodations_no": (
            hotel_accommodations_no
        ),

        "air_freight_required": (
            air_freight_required == "Yes"
        ),

        "air_freight_yes": (
            air_freight_yes
        ),

        "air_freight_no": (
            air_freight_no
        ),

        "ground_transportation_required": (
            ground_transportation_required == "Yes"
        ),

        "ground_transportation_yes": (
            ground_transportation_yes
        ),

        "ground_transportation_no": (
            ground_transportation_no
        ),

        "meals_incidentals_required": (
            meals_incidentals_required == "Yes"
        ),

        "meals_incidentals_yes": (
            meals_incidentals_yes
        ),

        "meals_incidentals_no": (
            meals_incidentals_no
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
