import streamlit as st

from utils.state_sync import (
    sync_linked_text_field,
    detect_manual_override,
)

from features.contracts.presentation.sections import (
    render_profile_autofill,
    render_travel_terms_section,
    render_merchandising_section,
    render_show_details_section,
)

def render_performance_contract_fields(
    key_prefix: str,
    container,
) -> dict:
    """
    Render the complete performance contract
    input form and collect normalized UI data.

    Responsibilities:
    - Render Streamlit form sections
    - Collect contract configuration data
    - Build per-show structures
    - Calculate financial projections
    - Return structured form payload
    """

    # Artist Profile Autofill
    render_profile_autofill(
        key_prefix,
        container,
    )

    st.markdown("### Core Details")

    col1, col2 = st.columns(2)

    # Left-side core contract fields
    with col1:

        company_name = st.text_input(
            "Company Name",
            key=f"{key_prefix}_company_name",
        )

        artist_key = (
            f"{key_prefix}_artist"
        )

        artist_touched_key = (
            f"{artist_key}_touched"
        )

        # Synchronize artist name with
        # company name until manually edited
        sync_linked_text_field(
            source_value=company_name,

            target_key=artist_key,

            touched_key=artist_touched_key,
        )
            
        artist = st.text_input(
            "Artist Name",
            key=artist_key,
        )

        # Detect manual override
        detect_manual_override(
            source_value=company_name,

            target_value=artist,

            touched_key=artist_touched_key,
        )

        purchaser_name = st.text_input(
            "Promoter / Purchasing Company",
            key=f"{key_prefix}_purchaser_name",
        )

        signatory_key = (
            f"{key_prefix}_signatory"
        )

        signatory_touched_key = (
            f"{signatory_key}_touched"
        )

        # Synchronize purchaser signatory
        # with purchaser name until manually edited
        sync_linked_text_field(
            source_value=purchaser_name,

            target_key=signatory_key,

            touched_key=signatory_touched_key,
        )

        signatory = st.text_input(
            "Purchaser Signatory",
            key=signatory_key,
        )

        # Detect manual override
        detect_manual_override(
            source_value=purchaser_name,

            target_value=signatory,

            touched_key=signatory_touched_key,
        )
            

    # Right-side event and fee fields
    with col2:

        venue = st.text_input(
            "Primary Venue",
            key=f"{key_prefix}_venue"
        )

        city_key = f"{key_prefix}_city"

        city = st.text_input(
            "Primary City",
            key=city_key,
        )

        date = st.date_input(
            "Effective Date",
            key=f"{key_prefix}_date"
        )

        signature_date = st.date_input(
            "Signature Date",
            value=date,
            key=f"{key_prefix}_signature_date",
        )

        fee_key = f"{key_prefix}_fee"

        # Initialize fee field
        if fee_key not in st.session_state:

            st.session_state[fee_key] = ""

        fee_input = st.text_input(  
            "Flat Guarantee",
            key=fee_key,
            placeholder="Enter amount in USD",
        )

        # Remove commas before conversion
        clean_fee = (
            fee_input
            .replace(",", "")
            .strip()
        )

        # Convert formatted value into float
        try:
            fee = (
                float(clean_fee)
                if clean_fee
                else 0
            )

        except ValueError:

            fee = 0

        ticketing_fee_percent = (
            st.number_input(
                "Ticketing Fee %",

                min_value=0.0,

                max_value=100.0,

                value=0.0,

                step=0.1,

                key=(
                    f"{key_prefix}"
                    f"_ticketing_fee_percent"
                ),
            )
        )

    # Address-related sections
    col3, col4 = st.columns(2)

    with col3:

        purchaser_address = st.text_area(
            "Purchaser Address",
            value=venue,
            key=f"{key_prefix}_purchaser_address",
        )

    with col4:

        company_address = st.text_area(
            "Company Address",
            value=venue,
            key=f"{key_prefix}_company_address",
        )

    st.markdown("### Show Setup")

    col5, col6, col7 = st.columns(3)

    # Global show configuration
    with col5:

        number_of_shows = int(
            st.selectbox(
                "Number of Shows",

                options=list(range(1, 13)),

                index=0,

                help=(
                    "Choose how many show "
                    "sections the contract "
                    "should generate."
                ),

                key=f"{key_prefix}_number_of_shows",
            )
        )

    with col6:

        show_length_value = st.number_input(
            "Default Show Length",

            min_value=1,

            value=90,
            
            step=1,

            key=f"{key_prefix}_show_length_value",
        )

        show_length_unit = st.selectbox(
            "Show Length Unit",
            options=[
                "Minutes",
                "Hours",
            ],

            key=f"{key_prefix}_show_length_unit",
        )

        unit = (
            show_length_unit[:-1]
            if show_length_value == 1
            else show_length_unit
        )

        show_length = (
            f"{show_length_value} "
            f"{unit}"
        )

    

    with col7:

        capacity = st.text_input(
            "Default Capacity",
            key=f"{key_prefix}_capacity",
        )


    # Travel & Terms Section
    travel_terms = (
        render_travel_terms_section(
            key_prefix
        )
    )

    # Extract normalized section values
    air_transportation = (
        travel_terms[
            "air_transportation"
        ]
    )

    hotel_accommodations = (
        travel_terms[
            "hotel_accommodations"
        ]
    )

    air_freight = (
        travel_terms[
            "air_freight"
        ]
    )

    ground_transportation = (
        travel_terms[
            "ground_transportation"
        ]
    )

    meals_incidentals = (
        travel_terms[
            "meals_incidentals"
        ]
    )

    complimentary_tickets = (
        travel_terms[
            "complimentary_tickets"
        ]
    )

    concessionaire_fee = (
        travel_terms[
            "concessionaire_fee"
        ]
    )

    seller = travel_terms["seller"]

    special_provisions = (
        travel_terms[
            "special_provisions"
        ]
    )

    production_catering = (
        travel_terms[
            "production_catering"
        ]
    )


    # Merchandising Section
    merchandising = (
        render_merchandising_section(
            key_prefix
        )
    )

    # Extract normalized merchandising values
    hard_merchandising = (
        merchandising[
            "hard_merchandising"
        ]
    )

    soft_merchandising = (
        merchandising[
            "soft_merchandising"
        ]
    )

    merchandising_terms = (
        merchandising[
            "merchandising_terms"
        ]
    )

    additional_addenda = (
        merchandising[
            "additional_addenda"
        ]
    )

    # Shared fallback notes used to initialize
    # per-show additional acts fields
    general_notes = st.text_area(
        "Default Additional Acts / Notes",
        key=f"{key_prefix}_notes",
    )

    # Buyer signature configuration
    buyer_name_key = (
        f"{key_prefix}_buyer_name"
    )

    buyer_name_touched_key = (
        f"{buyer_name_key}_touched"
    )

    # Synchronize buyer signature name
    # with purchaser signatory until
    # manually overridden
    sync_linked_text_field(
        source_value=signatory,

        target_key=buyer_name_key,

        touched_key=(
            buyer_name_touched_key
        ),
    )

    buyer_name = st.text_input(
        "Buyer Signature Name",
        key=buyer_name_key,
    )

    # Detect manual override
    detect_manual_override(
        source_value=signatory,

        target_value=buyer_name,

        touched_key=(
            buyer_name_touched_key
        ),
    )
    
    buyer_company_name = st.text_input(
        "Buyer Signature Company",
        value=company_name,
        key=f"{key_prefix}_buyer_company_name",
    )

    st.markdown("### Per-Show Details")

    # Return normalized form payload
    # consumed by the application layer
    # Render dynamic per-show
    # configuration sections
    show_details = (
        render_show_details_section(
            key_prefix=key_prefix,

            number_of_shows=(
                number_of_shows
            ),

            city=city,

            venue=venue,

            date=date,

            show_length=show_length,

            capacity=capacity,

            ticketing_fee_percent=(
                ticketing_fee_percent
            ),

            general_notes=general_notes,
        )
    )

    return {
        "artist": artist,
        "client": company_name,

        "purchaser_name": purchaser_name,
        "purchaser_address": purchaser_address,

        "signatory": signatory,

        "company_name": company_name,
        "company_address": company_address,

        "venue": venue,
        "date": date,
        "signature_date": signature_date,

        "city": city,
        "fee": fee,

        "ticketing_fee_percent": (
            ticketing_fee_percent
        ),

        "number_of_shows": (
            number_of_shows
        ),

        "show_length": show_length,
        "capacity": capacity,

        "notes": general_notes,

        # Travel and logistics
        "air_transportation": (
            air_transportation
        ),

        "hotel_accommodations": (
            hotel_accommodations
        ),

        "air_freight": air_freight,

        "ground_transportation": (
            ground_transportation
        ),

        "meals_incidentals": (
            meals_incidentals
        ),

        # Contract terms
        "special_provisions": (
            special_provisions
        ),

        "concessionaire_fee": (
            concessionaire_fee
        ),

        "seller": seller,

        "hard_merchandising": (
            hard_merchandising
        ),

        "soft_merchandising": (
            soft_merchandising
        ),

        "complimentary_tickets": (
            complimentary_tickets
        ),

        # Large text sections
        "production_catering": (
            production_catering
        ),

        "additional_addenda": (
            additional_addenda
        ),

        "merchandising_terms": (
            merchandising_terms
        ),

        # Buyer signature fields
        "buyer_name": buyer_name,

        "buyer_company_name": (
            buyer_company_name
        ),

        # Per-show configuration payload
        "shows": show_details,
    }
