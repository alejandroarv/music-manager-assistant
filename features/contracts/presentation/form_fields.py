import streamlit as st

# Default ticket pricing configuration used
# to initialize ticket scaling tables
DEFAULT_TICKET_ROWS = [
    ("Platinum", 400, 0, 57.38, 22952.00),
    ("Gold", 400, 0, 49.18, 19672.00),
    ("VIP", 100, 0, 40.98, 4098.00),
    ("Platea Oeste", 600, 0, 36.89, 22134.00),
    ("Platea Este", 1000, 0, 32.79, 32790.00),
    ("Popular", 1500, 0, 28.69, 43035.00),
]

def compute_ticket_totals(
    ticket_rows: list[dict]
) -> tuple[float, float]:
    """
    Calculate gross and net ticket revenue
    projections from ticket rows.
    """

    gross = sum(
        float(row.get("line_total", 0) or 0)
        for row in ticket_rows
    )

    # Gross and net are currently identical
    # but remain separated for future logic
    return gross, gross


def compute_line_total(
    total: float,
    comps_kills: float,
    price: float
) -> float:
    """
    Calculate sellable inventory revenue
    for a ticket tier.
    """

    sellable = max(
        float(total or 0)
        - float(comps_kills or 0),
        0.0,
    )

    return sellable * float(price or 0)


def compute_expense_totals(
    fixed_expenses: float,
    variable_expenses: float,
    net_potential: float,
) -> tuple[float, float, float, float]:
    """
    Calculate expense and profit projection values.
    """

    total_est_expenses = (
        float(fixed_expenses or 0)
        + float(variable_expenses or 0)
    )

    break_even = total_est_expenses

    amount_to_split = (
        float(net_potential or 0)
        - total_est_expenses
    )

    walkout_potential = amount_to_split

    return (
        break_even,
        total_est_expenses,
        amount_to_split,
        walkout_potential,
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

    # Retrieve all saved artist profiles
    profiles = (
        container.profile_service
        .get_all_profiles()
    )

    # Build dropdown options
    profile_names = [
        profile["name"] 
        for profile in profiles
    ]

    # Session-state key used to prevent
    # repeated autofill ovceerwriting edits
    last_profile_key = (
        f"{key_prefix}_last_profile"
    )

    # Artist profile selector
    selected_profile = st.selectbox(
        "Artist Profile",

        options=[
            "None",
            *profile_names,
        ],

        key=f"{key_prefix}_profile_selector",
      )
     # Only autofill when the selected
    # profile actually changes
    if (
        selected_profile != "None"
        and
        st.session_state.get(
            last_profile_key
        ) != selected_profile
    ):

        # Load selected artist profile
        profile = (
            container.profile_service
            .get_profile_by_artist(
                selected_profile
            )
        )

        if profile:

            # Convert profile into
            # reusable form defaults
            defaults = (
                container.profile_service
                .build_form_defaults(
                    profile
                )
            )

            # ==========================================
            # Autofill Core Contract Fields
            # ==========================================

            st.session_state[
                f"{key_prefix}_company_name"
            ] = defaults.get(
                "company_name",
                "",
            )

            st.session_state[
                f"{key_prefix}_artist"
            ] = defaults.get(
                "artist_name",
                "",
            )

            st.session_state[
                f"{key_prefix}_purchaser_name"
            ] = defaults.get(
                "purchaser_name",
                "",
            )

            st.session_state[
                f"{key_prefix}_purchaser_address"
            ] = defaults.get(
                "purchaser_address",
                "",
            )

            st.session_state[
                f"{key_prefix}_signatory"
            ] = defaults.get(
                "signatory",
                "",
            )

            st.session_state[
                f"{key_prefix}_company_address"
            ] = defaults.get(
                "company_address",
                "",
            )

            # ==========================================
            # Autofill Terms & Logistics
            # ==========================================

            st.session_state[
                f"{key_prefix}_air_transportation"
            ] = defaults.get(
                "air_transportation",
                "",
            )

            st.session_state[
                f"{key_prefix}_hotel_accommodations"
            ] = defaults.get(
                "hotel_accommodations",
                "",
            )

            st.session_state[
                f"{key_prefix}_ground_transportation"
            ] = defaults.get(
                "ground_transportation",
                "",
            )

            st.session_state[
                f"{key_prefix}_special_provisions"
            ] = defaults.get(
                "special_provisions",
                "",
            )

            st.session_state[
                f"{key_prefix}_production_catering"
            ] = defaults.get(
                "production_catering",
                "",
            )

            st.session_state[
                f"{key_prefix}_merchandising_terms"
            ] = defaults.get(
                "merchandising_terms",
                "",
            )

            # Save selected profile state
            # to prevent rerun overwrites
            st.session_state[
                last_profile_key
            ] = selected_profile

            # Force rerun so populated
            # values appear immediately
            st.rerun()

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

        # Initialize artist from company
        if artist_key not in st.session_state:

            st.session_state[
                artist_key
            ] = company_name

        # Keep synced until manually edited
        if (
            not st.session_state.get(
                artist_touched_key,
                False,
            )
        ):

            st.session_state[
                artist_key
            ] = company_name

        artist = st.text_input(
            "Artist Name",
            key=artist_key,
        )

        # Detect manual override
        if artist != company_name:

            st.session_state[
                artist_touched_key
            ] = True
        

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

        # Initialize from purchaser
        if signatory_key not in st.session_state:

            st.session_state[
                signatory_key
            ] = purchaser_name
        
        # Keep synced until manually edited
        if (
            not st.session_state.get(
                signatory_touched_key,
                False,
            )
        ):

            st.session_state[
                signatory_key
            ] = purchaser_name
        
        signatory = st.text_input(
            "Purchaser Signatory",
            key=signatory_key,
        )
        
        # Detect manual override
        if signatory != purchaser_name:

            st.session_state[
                signatory_touched_key
            ] = True

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
            f"{show_length_value}"
            f"{unit}"
        )

    

    with col7:

        capacity = st.text_input(
            "Default Capacity",
            key=f"{key_prefix}_capacity",
        )

    st.markdown("### Terms")

    col8, col9 = st.columns(2)

    # Travel and logistics fields
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

        complimentary_tickets = st.text_input(
            "Complimentary Tickets",
            key=f"{key_prefix}_complimentary_tickets",
        )

    # Business and merchandising fields
    with col9:

        concessionaire_fee = st.text_input(
            "Concessionaire Fee",
            key=f"{key_prefix}_concessionaire_fee",
        )

        seller = st.text_input(
            "Seller",
            key=f"{key_prefix}_seller",
        )

        special_provisions = st.text_area(
            "Special Provisions",
            key=f"{key_prefix}_special_provisions",
        )
    # Large free-text contract sections
    production_catering = st.text_area(
        "Production & Catering",
        key=f"{key_prefix}_production_catering",
    )

    st.markdown("### Merchandising")

    merch_col1, merch_col2 = st.columns(2)

    with merch_col1:

        hard_merchandising = st.selectbox(
            "Hard Mechandising",

            options=[
                "Allowed",
                "Restricted",
                "Not Allowed",
            ],

            key=f"{key_prefix}_hard_merchandising",
        )
    
    with merch_col2:

        soft_merchandising = st.selectbox(
            "Soft Merchandising",

            options=[
                "Allowed",
                "Restricted",
                "Not Allowed",
            ],

            key=f"{key_prefix}_soft_merchandising",
        )


    merchandising_terms = st.text_area(
        "Merchandising Terms",
        key=f"{key_prefix}_merchandising_terms",
    )

    additional_addenda = st.text_area(
        "Additional Addenda",
        key=f"{key_prefix}_additional_addenda",
    )

    # Shared fallback notes used to initialize
    # per-show additional acts fields
    general_notes = st.text_area(
        "Default Additional Acts / Notes",
        key=f"{key_prefix}_notes",
    )

    # Buyer signature configuration
    buyer_name = st.text_input(
        "Buyer Signature Name",
        value=signatory,
        key=f"{key_prefix}_buyer_name",
    )

    buyer_company_name = st.text_input(
        "Buyer Signature Company",
        value=company_name,
        key=f"{key_prefix}_buyer_company_name",
    )

    st.markdown("### Per-Show Details")

    # Container for normalized per-show structures
    show_details = []

    # Dynamically render show sections
    # based on configured show count
    for i in range(number_of_shows):

        with st.expander(
            f"Show {i + 1}",
            expanded=(i == 0)
        ):

            top_left, top_mid, top_right = st.columns(3)

            # Core venue and date fields
            with top_left:

                show_city_key = (
                    f"{key_prefix}_show_city_{i}"
                )

                show_city_touched_key = (
                    f"{show_city_key}_touched"
                )

                # Initialize city field
                if show_city_key not in st.session_state:

                    st.session_state[show_city_key] = (
                        city if i == 0 else ""
                    )

                if (
                    i == 0
                    and not st.session_state.get(
                        show_city_touched_key,
                        False,
                    )
                ):

                    st.session_state[show_city_key] = city

                show_city = st.text_input(
                    f"City {i + 1}",
                    key=show_city_key,
                )

                # Detect manual edit
                if i == 0 and show_city != city:

                    st.session_state[
                        show_city_touched_key
                    ] = True

                  
                show_venue_key = (
                    f"{key_prefix}_show_venue_{i}"
                )

                show_venue_touched_key = (
                    f"{show_venue_key}_touched"
                )

                # Initialize venue field
                if show_venue_key not in st.session_state:

                    st.session_state[show_venue_key] = (
                        venue if i == 0 else ""
                    )

                if (
                    i == 0
                    and not st.session_state.get(
                        show_venue_touched_key,
                        False,
                    )
                ):

                    st.session_state[show_venue_key] = venue

                show_venue = st.text_input(
                    f"Venue {i + 1}",
                    key=show_venue_key,
                )

                # Detect manual edit
                if i == 0 and show_venue != venue:

                    st.session_state[
                        show_venue_touched_key
                    ] = True



                show_date_key = (
                    f"{key_prefix}_show_date_{i}"  
                )

                show_date_touched_key = (
                    f"{show_date_key}_touched"
                )

                # Initialize date field
                if show_date_key not in st.session_state:

                    st.session_state[show_date_key] = date
                
                # Keep show 1 synced until manually edit
                if (
                    i == 0
                    and not st.session_state.get(
                        show_date_touched_key,
                        False,
                    )
                ):

                    st.session_state[show_date_key] = date

                show_date = st.date_input(
                    f"Date {i + 1}",
                    key=show_date_key,
                )

                # Detect manual edit
                if i == 0 and show_date != date:

                    st.session_state[
                        show_date_touched_key
                    ] = True

            # Scheduling and capacity fields
            with top_mid:

                show_time = st.text_input(
                    f"Schedule {i + 1}",
                    key=f"{key_prefix}_show_time_{i}",
                )

                show_length_key = (
                    f"{key_prefix}_show_length_{i}"
                )  

                show_length_touched_key = (
                    f"{show_length_key}_touched"
                )

                # Initialize show length field
                if show_length_key not in st.session_state:

                    st.session_state[show_length_key] = (
                        show_length if i == 0 else ""
                    )

                # Keep show 1 synced until manually edit
                if (
                    i == 0
                    and not st.session_state.get(
                        show_length_touched_key,
                        False,
                    )
                ):

                    st.session_state[
                        show_length_key
                    ] = show_length
                
                show_length_value = st.text_input(
                    f"Show Length {i + 1}",
                    key=show_length_key,
                )

                # Detect manual edit to show length

                if (
                    i == 0
                    and show_length_value != show_length
                ):

                    st.session_state[
                        show_length_touched_key
                    ] = True    
                

                capacity_key = (
                    f"{key_prefix}_capacity_{i}"
                )
                capacity_touched_key = (
                    f"{capacity_key}_touched"
                )

                # Initialize capacity field
                if capacity_key not in st.session_state:

                    st.session_state[capacity_key] = (
                        capacity if i == 0 else ""
                    )

                # Keep show 1 synced until manually edit
                if (
                    i == 0
                    and not st.session_state.get(
                        capacity_touched_key,
                        False,
                    )
                ):

                    st.session_state[
                        capacity_key
                    ] = capacity
                
                show_capacity = st.text_input(
                    f"Capacity {i + 1}",
                    key=capacity_key,
                )
                # Detect manual edit to capacity
                if (
                    i == 0
                    and show_capacity != capacity
                ):

                    st.session_state[
                        capacity_touched_key
                    ] = True

            # Per-show notes and support acts
            with top_right:

                show_notes_key = (
                    f"{key_prefix}_show_notes_{i}"
                )

                show_notes_touched_key = (
                    f"{show_notes_key}_touched"
                )

                # Initialize ntoes field
                if show_notes_key not in st.session_state:

                    st.session_state[show_notes_key] = (
                        general_notes if i == 0 else ""
                    )
                
                # Keep SHow 1 synced until manually edit
                if (
                    i == 0
                    and not st.session_state.get(
                        show_notes_touched_key,
                        False,
                    )
                ):

                    st.session_state[show_notes_key] = (
                        general_notes
                    )
                
                show_notes = st.text_area(
                    f"Additional Acts / Notes {i + 1}",
                    key=show_notes_key, 
                )

                if i == 0 and show_notes != general_notes:

                    st.session_state[
                        show_notes_touched_key
                    ] = True




            # Expand advanced financial sections
            # automatically for multi-show contracts
            advanced_label = (
                "Advanced Pricing & Expenses"
                if number_of_shows == 1
                else "Ticket Scaling & Expense Table"
            )

            advanced_expanded = (
                number_of_shows > 1
            )

            gross_potential = 0.0
            net_potential = 0.0

            with st.expander(
                advanced_label,
                expanded=advanced_expanded
            ):

                st.markdown("Ticket Scaling")

                # Automatically calculate ticket
                # line totals from inventory data
                auto_ticket_math = st.checkbox(
                    "Auto-calculate ticket math",

                    value=True,

                    key=(
                        f"{key_prefix}"
                        f"_auto_ticket_math_{i}"
                    ),

                    help=(
                        "Calculates each line total "
                        "from Total - Comps/Kills "
                        "times Price."
                    ),
                )

                ticket_rows = []

                # Render ticket pricing tiers
                for row_index, (
                    label,
                    total_default,
                    comps_default,
                    price_default,
                    line_total_default,
                ) in enumerate(DEFAULT_TICKET_ROWS):

                    t1, t2, t3, t4 = st.columns(4)

                    with t1:

                        total_value = st.number_input(
                            f"{label} Total {i + 1}",

                            min_value=0,

                            value=total_default,

                            key=(
                                f"{key_prefix}"
                                f"_ticket_total_"
                                f"{i}_{row_index}"
                            ),
                        )

                    with t2:

                        comps_value = st.number_input(
                            f"{label} Comps/Kills {i + 1}",

                            min_value=0,

                            value=comps_default,

                            key=(
                                f"{key_prefix}"
                                f"_ticket_comps_"
                                f"{i}_{row_index}"
                            ),
                        )

                    with t3:

                        price_value = st.number_input(
                            f"{label} Price {i + 1}",

                            min_value=0.0,

                            value=float(price_default),

                            step=0.01,

                            key=(
                                f"{key_prefix}"
                                f"_ticket_price_"
                                f"{i}_{row_index}"
                            ),
                        )

                    with t4:

                        # Calculate projected ticket
                        # revenue for the pricing tier
                        computed_line_total = (
                            compute_line_total(
                                total_value,
                                comps_value,
                                price_value,
                            )
                        )

                        if auto_ticket_math:

                            line_total_value = (
                                computed_line_total
                            )

                            st.caption(
                                f"{label} Line Total: "
                                f"${line_total_value:,.2f}"
                            )

                        else:

                            line_total_value = (
                                st.number_input(
                                    f"{label} Line Total "
                                    f"{i + 1}",

                                    min_value=0.0,

                                    value=float(
                                        line_total_default
                                    ),

                                    step=0.01,

                                    key=(
                                        f"{key_prefix}"
                                        f"_ticket_line_total_"
                                        f"{i}_{row_index}"
                                    ),
                                )
                            )

                    # Store normalized ticket row data
                    ticket_rows.append(
                        {
                            "label": label,
                            "total": total_value,
                            "comps_kills": comps_value,
                            "price": price_value,
                            "line_total": line_total_value,
                        }
                    )

                # Calculate aggregate revenue projections
                auto_gross, auto_net = (
                    compute_ticket_totals(
                        ticket_rows
                    )
                )

                auto_calc_enabled = st.checkbox(
                    "Auto-calculate Gross/Net "
                    "from ticket rows",

                    value=True,

                    key=f"{key_prefix}_auto_calc_{i}",
                )

                if auto_calc_enabled:

                    gross_potential = auto_gross
                    net_potential = auto_net

                    st.caption(
                        f"Gross Potential: "
                        f"${gross_potential:,.2f}"
                    )

                    st.caption(
                        f"Net Potential: "
                        f"${net_potential:,.2f}"
                    )

                else:

                    gross_potential = st.number_input(
                        f"Gross Potential {i + 1}",

                        min_value=0.0,

                        step=100.0,

                        value=float(gross_potential),

                        key=(
                            f"{key_prefix}"
                            f"_gross_override_{i}"
                        ),
                    )

                    net_potential = st.number_input(
                        f"Net Potential {i + 1}",

                        min_value=0.0,

                        step=100.0,

                        value=float(net_potential),

                        key=(
                            f"{key_prefix}"
                            f"_net_override_{i}"
                        ),
                    )

                st.markdown("Expense Table")

                # Automatically calculate expense
                # and profitability projections
                auto_expense_math = st.checkbox(
                    "Auto-calculate expense math",

                    value=True,

                    key=(
                        f"{key_prefix}"
                        f"_auto_expense_math_{i}"
                    ),

                    help=(
                        "Calculates Break Even, "
                        "Total Estimated Expenses, "
                        "Amount to Split, and "
                        "Walkout Potential."
                    ),
                )

                e1, e2, e3 = st.columns(3)

                # Expense input fields
                with e1:

                    fixed_expenses = st.number_input(
                        f"Fixed Expenses {i + 1}",

                        min_value=0.0,

                        step=100.0,

                        key=(
                            f"{key_prefix}"
                            f"_fixed_expenses_{i}"
                        ),
                    )

                    variable_expenses = st.number_input(
                        f"Variable Expenses {i + 1}",

                        min_value=0.0,

                        step=100.0,

                        key=(
                            f"{key_prefix}"
                            f"_variable_expenses_{i}"
                        ),
                    )

                # Break-even and estimated expense calculations
                with e2:

                    (
                        computed_break_even,
                        computed_total_est_expenses,
                        computed_amount_to_split,
                        computed_walkout_potential,
                    ) = compute_expense_totals(
                        fixed_expenses,
                        variable_expenses,
                        net_potential,
                    )

                    if auto_expense_math:

                        break_even = (
                            computed_break_even
                        )

                        total_est_expenses = (
                            computed_total_est_expenses
                        )

                        st.caption(
                            f"Break Even: "
                            f"${break_even:,.2f}"
                        )

                        st.caption(
                            "Total Estimated Expenses: "
                            f"${total_est_expenses:,.2f}"
                        )

                    else:

                        break_even = st.number_input(
                            f"Break Even {i + 1}",

                            min_value=0.0,

                            step=100.0,

                            value=float(
                                computed_break_even
                            ),

                            key=(
                                f"{key_prefix}"
                                f"_break_even_{i}"
                            ),
                        )

                        total_est_expenses = (
                            st.number_input(
                                "Total Estimated Expenses "
                                f"{i + 1}",

                                min_value=0.0,

                                step=100.0,

                                value=float(
                                    computed_total_est_expenses
                                ),

                                key=(
                                    f"{key_prefix}"
                                    f"_total_est_expenses_{i}"
                                ),
                            )
                        )

                # Profit-sharing and walkout projections
                with e3:

                    if auto_expense_math:

                        amount_to_split = (
                            computed_amount_to_split
                        )

                        walkout_potential = (
                            computed_walkout_potential
                        )

                        st.caption(
                            "Amount to Split: "
                            f"${amount_to_split:,.2f}"
                        )

                        st.caption(
                            "Walkout Potential: "
                            f"${walkout_potential:,.2f}"
                        )

                    else:

                        amount_to_split = (
                            st.number_input(
                                f"Amount to Split {i + 1}",

                                step=100.0,

                                value=float(
                                    computed_amount_to_split
                                ),

                                key=(
                                    f"{key_prefix}"
                                    f"_amount_to_split_{i}"
                                ),
                            )
                        )

                        walkout_potential = (
                            st.number_input(
                                f"Walkout Potential {i + 1}",

                                step=100.0,

                                value=float(
                                    computed_walkout_potential
                                ),

                                key=(
                                    f"{key_prefix}"
                                    f"_walkout_potential_{i}"
                                ),
                            )
                        )

            # Store normalized per-show configuration
            show_details.append(
                {
                    "city": show_city,
                    "venue": show_venue,
                    "date": show_date,
                    "time": show_time,

                    "show_length": (
                        show_length_value
                    ),

                    "capacity": show_capacity,

                    "notes": show_notes,

                    # Ticket scaling and projections
                    "ticket_rows": ticket_rows,

                    "gross_potential": (
                        gross_potential
                    ),

                    "net_potential": (
                        net_potential
                    ),

                    # Expense breakdown projections
                    "expenses": {
                        "fixed_expenses": (
                            fixed_expenses
                        ),

                        "variable_expenses": (
                            variable_expenses
                        ),

                        "break_even": (
                            break_even
                        ),

                        "net_potential": (
                            net_potential
                        ),

                        "total_est_expenses": (
                            total_est_expenses
                        ),

                        "amount_to_split": (
                            amount_to_split
                        ),

                        "walkout_potential": (
                            walkout_potential
                        ),
                    },
                }
            )

    # Return normalized form payload
    # consumed by the application layer
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