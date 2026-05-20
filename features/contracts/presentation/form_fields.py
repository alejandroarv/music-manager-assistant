import streamlit as st


DEFAULT_TICKET_ROWS = [
    ("Platinum", 400, 0, 57.38, 22952.00),
    ("Gold", 400, 0, 49.18, 19672.00),
    ("VIP", 100, 0, 40.98, 4098.00),
    ("Platea Oeste", 600, 0, 36.89, 22134.00),
    ("Platea Este", 1000, 0, 32.79, 32790.00),
    ("Popular", 1500, 0, 28.69, 43035.00),
]


def compute_ticket_totals(ticket_rows: list[dict]) -> tuple[float, float]:
    gross = sum(float(row.get("line_total", 0) or 0) for row in ticket_rows)
    return gross, gross


def compute_line_total(total: float, comps_kills: float, price: float) -> float:
    sellable = max(float(total or 0) - float(comps_kills or 0), 0.0)
    return sellable * float(price or 0)


def compute_expense_totals(
    fixed_expenses: float,
    variable_expenses: float,
    net_potential: float,
) -> tuple[float, float, float, float]:
    total_est_expenses = float(fixed_expenses or 0) + float(variable_expenses or 0)
    break_even = total_est_expenses
    amount_to_split = float(net_potential or 0) - total_est_expenses
    walkout_potential = amount_to_split
    return (
        break_even,
        total_est_expenses,
        amount_to_split,
        walkout_potential,
    )


def render_performance_contract_fields(key_prefix: str) -> dict:
    st.markdown("### Core Details")
    col1, col2 = st.columns(2)

    with col1:
        artist = st.text_input("Artist Name", key=f"{key_prefix}_artist")
        client = st.text_input("Client / Promoter", key=f"{key_prefix}_client")
        purchaser_name = st.text_input(
            "Purchaser Name",
            value=client,
            key=f"{key_prefix}_purchaser_name",
        )
        company_name = st.text_input(
            "Company Name",
            value=client,
            key=f"{key_prefix}_company_name",
        )
        signatory = st.text_input(
            "Purchaser Signatory",
            value=purchaser_name,
            key=f"{key_prefix}_signatory",
        )

    with col2:
        venue = st.text_input("Primary Venue", key=f"{key_prefix}_venue")
        city = st.text_input("Primary City", key=f"{key_prefix}_city")
        date = st.date_input("Effective Date", key=f"{key_prefix}_date")
        signature_date = st.date_input(
            "Signature Date",
            value=date,
            key=f"{key_prefix}_signature_date",
        )
        fee = st.number_input(
            "Flat Guarantee",
            min_value=0.0,
            step=100.0,
            key=f"{key_prefix}_fee",
        )

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
    with col5:
        number_of_shows = int(
            st.selectbox(
                "Number of Shows",
                options=list(range(1, 13)),
                index=0,
                help="Choose how many show sections the contract should generate.",
                key=f"{key_prefix}_number_of_shows",
            )
        )
    with col6:
        show_length = st.text_input(
            "Default Show Length",
            key=f"{key_prefix}_show_length",
        )
    with col7:
        capacity = st.text_input(
            "Default Capacity",
            key=f"{key_prefix}_capacity",
        )

    st.markdown("### Terms")
    col8, col9 = st.columns(2)
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
    with col9:
        concessionaire_fee = st.text_input(
            "Concessionaire Fee",
            key=f"{key_prefix}_concessionaire_fee",
        )
        seller = st.text_input(
            "Seller",
            key=f"{key_prefix}_seller",
        )
        hard_merchandising = st.text_input(
            "Hard Merchandising",
            key=f"{key_prefix}_hard_merchandising",
        )
        soft_merchandising = st.text_input(
            "Soft Merchandising",
            key=f"{key_prefix}_soft_merchandising",
        )
        special_provisions = st.text_area(
            "Special Provisions",
            key=f"{key_prefix}_special_provisions",
        )

    production_catering = st.text_area(
        "Production & Catering",
        key=f"{key_prefix}_production_catering",
    )
    merchandising_terms = st.text_area(
        "Merchandising Terms",
        key=f"{key_prefix}_merchandising_terms",
    )
    additional_addenda = st.text_area(
        "Additional Addenda",
        key=f"{key_prefix}_additional_addenda",
    )

    general_notes = st.text_area(
        "Default Additional Acts / Notes",
        key=f"{key_prefix}_notes",
    )

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
    show_details = []
    for i in range(number_of_shows):
        with st.expander(f"Show {i + 1}", expanded=(i == 0)):
            top_left, top_mid, top_right = st.columns(3)
            with top_left:
                show_city = st.text_input(
                    f"City {i + 1}",
                    value=city,
                    key=f"{key_prefix}_show_city_{i}",
                )
                show_venue = st.text_input(
                    f"Venue {i + 1}",
                    value=venue,
                    key=f"{key_prefix}_show_venue_{i}",
                )
                show_date = st.date_input(
                    f"Date {i + 1}",
                    value=date,
                    key=f"{key_prefix}_show_date_{i}",
                )
            with top_mid:
                show_time = st.text_input(
                    f"Schedule {i + 1}",
                    key=f"{key_prefix}_show_time_{i}",
                )
                show_length_value = st.text_input(
                    f"Show Length {i + 1}",
                    key=f"{key_prefix}_show_length_{i}",
                )
                show_capacity = st.text_input(
                    f"Capacity {i + 1}",
                    key=f"{key_prefix}_show_capacity_{i}",
                )
            with top_right:
                show_notes = st.text_area(
                    f"Additional Acts / Notes {i + 1}",
                    value=general_notes,
                    key=f"{key_prefix}_show_notes_{i}",
                )

            advanced_label = (
                "Advanced Pricing & Expenses"
                if number_of_shows == 1
                else "Ticket Scaling & Expense Table"
            )
            advanced_expanded = number_of_shows > 1
            gross_potential = 0.0
            net_potential = 0.0

            with st.expander(advanced_label, expanded=advanced_expanded):
                st.markdown("Ticket Scaling")
                auto_ticket_math = st.checkbox(
                    "Auto-calculate ticket math",
                    value=True,
                    key=f"{key_prefix}_auto_ticket_math_{i}",
                    help="Calculates each line total from Total - Comps/Kills times Price.",
                )
                ticket_rows = []
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
                            key=f"{key_prefix}_ticket_total_{i}_{row_index}",
                        )
                    with t2:
                        comps_value = st.number_input(
                            f"{label} Comps/Kills {i + 1}",
                            min_value=0,
                            value=comps_default,
                            key=f"{key_prefix}_ticket_comps_{i}_{row_index}",
                        )
                    with t3:
                        price_value = st.number_input(
                            f"{label} Price {i + 1}",
                            min_value=0.0,
                            value=float(price_default),
                            step=0.01,
                            key=f"{key_prefix}_ticket_price_{i}_{row_index}",
                        )
                    with t4:
                        computed_line_total = compute_line_total(
                            total_value,
                            comps_value,
                            price_value,
                        )
                        if auto_ticket_math:
                            line_total_value = computed_line_total
                            st.caption(f"{label} Line Total: ${line_total_value:,.2f}")
                        else:
                            line_total_value = st.number_input(
                                f"{label} Line Total {i + 1}",
                                min_value=0.0,
                                value=float(line_total_default),
                                step=0.01,
                                key=f"{key_prefix}_ticket_line_total_{i}_{row_index}",
                            )
                    ticket_rows.append(
                        {
                            "label": label,
                            "total": total_value,
                            "comps_kills": comps_value,
                            "price": price_value,
                            "line_total": line_total_value,
                        }
                    )

                auto_gross, auto_net = compute_ticket_totals(ticket_rows)
                auto_calc_enabled = st.checkbox(
                    "Auto-calculate Gross/Net from ticket rows",
                    value=True,
                    key=f"{key_prefix}_auto_calc_{i}",
                )
                if auto_calc_enabled:
                    gross_potential = auto_gross
                    net_potential = auto_net
                    st.caption(f"Gross Potential: ${gross_potential:,.2f}")
                    st.caption(f"Net Potential: ${net_potential:,.2f}")
                else:
                    gross_potential = st.number_input(
                        f"Gross Potential {i + 1}",
                        min_value=0.0,
                        step=100.0,
                        value=float(gross_potential),
                        key=f"{key_prefix}_gross_override_{i}",
                    )
                    net_potential = st.number_input(
                        f"Net Potential {i + 1}",
                        min_value=0.0,
                        step=100.0,
                        value=float(net_potential),
                        key=f"{key_prefix}_net_override_{i}",
                    )

                st.markdown("Expense Table")
                auto_expense_math = st.checkbox(
                    "Auto-calculate expense math",
                    value=True,
                    key=f"{key_prefix}_auto_expense_math_{i}",
                    help="Calculates Break Even, Total Estimated Expenses, Amount to Split, and Walkout Potential.",
                )
                e1, e2, e3 = st.columns(3)
                with e1:
                    fixed_expenses = st.number_input(
                        f"Fixed Expenses {i + 1}",
                        min_value=0.0,
                        step=100.0,
                        key=f"{key_prefix}_fixed_expenses_{i}",
                    )
                    variable_expenses = st.number_input(
                        f"Variable Expenses {i + 1}",
                        min_value=0.0,
                        step=100.0,
                        key=f"{key_prefix}_variable_expenses_{i}",
                    )
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
                        break_even = computed_break_even
                        total_est_expenses = computed_total_est_expenses
                        st.caption(f"Break Even: ${break_even:,.2f}")
                        st.caption(
                            f"Total Estimated Expenses: ${total_est_expenses:,.2f}"
                        )
                    else:
                        break_even = st.number_input(
                            f"Break Even {i + 1}",
                            min_value=0.0,
                            step=100.0,
                            value=float(computed_break_even),
                            key=f"{key_prefix}_break_even_{i}",
                        )
                        total_est_expenses = st.number_input(
                            f"Total Estimated Expenses {i + 1}",
                            min_value=0.0,
                            step=100.0,
                            value=float(computed_total_est_expenses),
                            key=f"{key_prefix}_total_est_expenses_{i}",
                        )
                with e3:
                    if auto_expense_math:
                        amount_to_split = computed_amount_to_split
                        walkout_potential = computed_walkout_potential
                        st.caption(f"Amount to Split: ${amount_to_split:,.2f}")
                        st.caption(
                            f"Walkout Potential: ${walkout_potential:,.2f}"
                        )
                    else:
                        amount_to_split = st.number_input(
                            f"Amount to Split {i + 1}",
                            step=100.0,
                            value=float(computed_amount_to_split),
                            key=f"{key_prefix}_amount_to_split_{i}",
                        )
                        walkout_potential = st.number_input(
                            f"Walkout Potential {i + 1}",
                            step=100.0,
                            value=float(computed_walkout_potential),
                            key=f"{key_prefix}_walkout_potential_{i}",
                        )

            show_details.append(
                {
                    "city": show_city,
                    "venue": show_venue,
                    "date": show_date,
                    "time": show_time,
                    "show_length": show_length_value,
                    "capacity": show_capacity,
                    "notes": show_notes,
                    "ticket_rows": ticket_rows,
                    "gross_potential": gross_potential,
                    "net_potential": net_potential,
                    "expenses": {
                        "fixed_expenses": fixed_expenses,
                        "variable_expenses": variable_expenses,
                        "break_even": break_even,
                        "net_potential": net_potential,
                        "total_est_expenses": total_est_expenses,
                        "amount_to_split": amount_to_split,
                        "walkout_potential": walkout_potential,
                    },
                }
            )

    return {
        "artist": artist,
        "client": client,
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
        "number_of_shows": number_of_shows,
        "show_length": show_length,
        "capacity": capacity,
        "notes": general_notes,
        "air_transportation": air_transportation,
        "hotel_accommodations": hotel_accommodations,
        "air_freight": air_freight,
        "ground_transportation": ground_transportation,
        "meals_incidentals": meals_incidentals,
        "special_provisions": special_provisions,
        "concessionaire_fee": concessionaire_fee,
        "seller": seller,
        "hard_merchandising": hard_merchandising,
        "soft_merchandising": soft_merchandising,
        "complimentary_tickets": complimentary_tickets,
        "production_catering": production_catering,
        "additional_addenda": additional_addenda,
        "merchandising_terms": merchandising_terms,
        "buyer_name": buyer_name,
        "buyer_company_name": buyer_company_name,
        "shows": show_details,
    }
