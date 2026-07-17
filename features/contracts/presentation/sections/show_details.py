# features/contracts/presentation/sections/show_details.py

# Streamlit UI framework
import streamlit as st

# Shared synchronization utilities
from utils.state_sync import (
    detect_manual_override,
)

from utils.show_sync import (
    initialize_show_sync,
)

from features.contracts.presentation.sections.venue_profile_autofill import (
    render_venue_profile_autofill,
)

from features.contracts.domain.logic import (
    compute_ticket_totals,
    compute_line_total,
    compute_walkout_potential,
    compute_expense_totals,
)

from features.contracts.presentation.sections.expense_table import (
    render_expense_table,
)

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

def render_show_details_section(
    key_prefix,
    container,
    number_of_shows,
    city,
    venue,
    venue_address,
    date,
    show_length,
    capacity_defaults,
    general_notes,
    deal_type,
    flat_guarantee,
    percentage,
    deal_basis,
):
    """
    Render per-show configuration sections.

    Responsibilities:
    - render dynamic show sections
    - synchronize default values
    - collect ticket scaling data
    - calculate projections
    - return normalized show payloads
    """
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

                show_venue_key = (
                    f"{key_prefix}_show_venue_{i}"
                )

                show_venue_touched_key = (
                    f"{show_venue_key}_touched"
                )

                show_venue_address_key = (
                    f"{key_prefix}_show_venue_address_{i}"
                )

                show_venue_address_touched_key = (
                    f"{show_venue_address_key}_touched"
                )

                capacity_key = (
                    f"{key_prefix}_capacity_{i}"
                )

                capacity_touched_key = (
                    f"{capacity_key}_touched"
                )

                selected_venue_profile = (
                    render_venue_profile_autofill(
                        key_prefix=(
                            f"{key_prefix}_show_{i}"
                        ),

                        container=container,

                        venue_key=show_venue_key,

                        city_key=show_city_key,

                        venue_address_key=(
                            show_venue_address_key
                        ),

                        capacity_key=capacity_key,
                    )
                )

                venue_source = (
                    selected_venue_profile.venue_name
                    if selected_venue_profile
                    else venue
                )

                city_source = (
                    selected_venue_profile.city
                    if selected_venue_profile
                    else city
                )

                venue_address_source = (
                    selected_venue_profile.venue_address
                    if selected_venue_profile
                    else venue_address
                )

                capacity_source = (
                    selected_venue_profile.venue_capacity
                    if selected_venue_profile
                    else (
                        capacity_defaults[i]
                        if i < len(capacity_defaults)
                        else ""
                    )
                )

                # Initialize synchronized
                # show city state
                initialize_show_sync(
                    i=i,

                    source_value=city_source,

                    target_key=show_city_key,

                    touched_key=(
                        show_city_touched_key
                    ),
                )

                show_city = st.text_input(
                    f"City {i + 1}",
                    key=show_city_key,
                )

                # Detect manual override
                detect_manual_override(
                    source_value=city_source,

                    target_value=show_city,

                    touched_key=(
                        show_city_touched_key
                    ),
                )
                  
                # Initialize synchronized
                # show venue state
                initialize_show_sync(
                    i=i,

                    source_value=venue_source,

                    target_key=show_venue_key,

                    touched_key=(
                        show_venue_touched_key
                    ),
                )


                show_venue = st.text_input(
                    f"Venue {i + 1}",
                    key=show_venue_key,
                )

                initialize_show_sync(
                    i=i,

                    source_value=venue_address_source,

                    target_key=(
                        show_venue_address_key
                    ),

                    touched_key=(
                        show_venue_address_touched_key
                    ),
                )

                show_venue_address = st.text_input(
                    f"Venue Address {i + 1}",
                    key=show_venue_address_key,
                )

                # Detect manual override
                detect_manual_override(
                    source_value=venue_source,

                    target_value=show_venue,

                    touched_key=(
                        show_venue_touched_key
                    ),
                )

                # Detect manual override
                detect_manual_override(
                    source_value=(
                        venue_address_source
                    ),

                    target_value=(
                        show_venue_address
                    ),

                    touched_key=(
                        show_venue_address_touched_key
                    ),
                )

                show_date_key = (
                    f"{key_prefix}_show_date_{i}"  
                )

                show_date_touched_key = (
                    f"{show_date_key}_touched"
                )

                # Initialize synchronized
                # show date state
                initialize_show_sync(
                    i=i,

                    source_value=date,

                    target_key=show_date_key,

                    touched_key=(
                        show_date_touched_key
                    ),

                    fallback_value=date,
                )
                    
                show_date = st.date_input(
                    f"Date {i + 1}",
                    key=show_date_key,
                )

                # Detect manual override
                detect_manual_override(
                    source_value=date,

                    target_value=show_date,

                    touched_key=(
                        show_date_touched_key
                    ),
                )

            # Scheduling and capacity fields
            with top_mid:

                schedule_count = st.number_input(
                    f"Schedule Entries {i + 1}",

                    min_value=1,

                    max_value=10,

                    value=1,

                    step=1,

                    key=(
                        f"{key_prefix}"
                        f"_schedule_count_{i}"
                    ),
                )

                schedule_rows = []

                st.markdown(
                    "##### Schedule"
                )

                for schedule_index in range(
                    schedule_count
                ):

                    s1, s2 = st.columns(2)

                    with s1:

                        schedule_type = (
                            st.text_input(
                                (
                                    "Schedule Type "
                                    f"{schedule_index + 1}"
                                ),

                                key=(
                                    f"{key_prefix}"
                                    f"_schedule_type_"
                                    f"{i}_{schedule_index}"
                                ),
                            )
                        )

                    with s2:

                        schedule_time = (
                            st.text_input(
                                (
                                    "Schedule Time "
                                    f"{schedule_index + 1}"
                                ),

                                key=(
                                    f"{key_prefix}"
                                    f"_schedule_time_"
                                    f"{i}_{schedule_index}"
                                ),
                            )
                        )

                    schedule_rows.append(
                        {
                            "type": (
                                schedule_type
                            ),

                            "time": (
                                schedule_time
                            ),
                        }
                    )

                show_length_key = (
                    f"{key_prefix}_show_length_{i}"
                )  

                show_length_touched_key = (
                    f"{show_length_key}_touched"
                )

                # Initialize synchronized
                # show length state
                initialize_show_sync(
                    i=i,

                    source_value=show_length,

                    target_key=show_length_key,

                    touched_key=(
                        show_length_touched_key
                    ),
                )
                
                show_length_value = st.text_input(
                    f"Show Length {i + 1}",
                    key=show_length_key,
                )

                # Detect manual override
                detect_manual_override(
                    source_value=show_length,

                    target_value=(
                        show_length_value
                    ),

                    touched_key=(
                        show_length_touched_key
                    ),
                )

                # Initialize synchronized
                # show capacity state
                initialize_show_sync(
                    i=i,

                    source_value=capacity_source,

                    target_key=capacity_key,

                    touched_key=(
                        capacity_touched_key
                    ),
                )
                
                show_capacity = st.text_input(
                    f"Capacity {i + 1}",
                    key=capacity_key,
                )
                # Detect manual override
                detect_manual_override(
                    source_value=capacity_source,

                    target_value=show_capacity,

                    touched_key=(
                        capacity_touched_key
                    ),
                )

            # Per-show notes and support acts
            with top_right:

                show_notes_key = (
                    f"{key_prefix}_show_notes_{i}"
                )

                show_notes_touched_key = (
                    f"{show_notes_key}_touched"
                )

                # Initialize synchronized
                # show notes state
                initialize_show_sync(
                    i=i,

                    source_value=general_notes,

                    target_key=show_notes_key,

                    touched_key=(
                        show_notes_touched_key
                    ),
                )
                
                show_notes = st.text_area(
                    f"Additional Acts / Notes {i + 1}",
                    key=show_notes_key, 
                )

                # Detect manual override
                detect_manual_override(
                    source_value=general_notes,

                    target_value=show_notes,

                    touched_key=(
                        show_notes_touched_key
                    ),
                )

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

                ticketing_fee_percent = (
                    st.number_input(
                        f"Ticketing Fee % {i + 1}",

                        min_value=0.0,

                        max_value=100.0,

                        value=0.0,

                        step=0.1,

                        key=(
                            f"{key_prefix}"
                            f"_ticketing_fee_percent_{i}"
                        ),
                    )
                )

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
                auto_gross, _ = (
                    compute_ticket_totals(
                        ticket_rows
                    )
                )

                ticketing_fee_amount = (
                    auto_gross
                    * (
                        ticketing_fee_percent
                        / 100
                    )
                )

                st.caption(
                    f"Ticketing Fee: "
                    f"${ticketing_fee_amount:,.2f}"
                )
                
                auto_net = (
                    auto_gross
                    - ticketing_fee_amount
                )

                include_merchandising = (
                    st.checkbox(
                        "Include Merchandising Revenue",

                        value=False,

                        key=(
                            f"{key_prefix}"
                            f"_include_merch_{i}"
                        ),
                    )
                )

                merchandising_revenue = (
                    st.number_input(
                        f"Merchandising Revenue {i + 1}",

                        min_value=0.0,

                        step=100.0,

                        value=0.0,

                        disabled=(
                            not include_merchandising
                        ),

                        key=(
                            f"{key_prefix}"
                            f"_merch_revenue_{i}"
                        ),
                    )
                )

                auto_calc_enabled = st.checkbox(
                    "Auto-calculate Gross/Net "
                    "from ticket rows",

                    value=True,

                    key=f"{key_prefix}_auto_calc_{i}",
                )

                if include_merchandising:

                    auto_gross += (
                        merchandising_revenue
                    )

                    auto_net += (
                        merchandising_revenue
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


                    fixed_rows, fixed_expenses = (
                        render_expense_table(
                            key_prefix=key_prefix,

                            show_index=i,

                            expense_category="fixed",
                        )
                    )

                    variable_rows, variable_expenses = (
                        render_expense_table(
                            key_prefix=key_prefix,

                            show_index=i,

                            expense_category="variable",
                        )
                    )

                # Break-even and estimated expense calculations
                with e2:
                    
                    st.write(
                        "Deal Debug",
                        {
                            "deal_type": deal_type,
                            "flat_guarantee": flat_guarantee,
                            "percentage": percentage,
                            "deal_basis": deal_basis,
                            "gross": gross_potential,
                            "net": net_potential,
                        },
                    )

                    computed_walkout_potential = (
                        compute_walkout_potential(
                            deal_type=deal_type,
                            flat_guarantee=flat_guarantee,
                            percentage=percentage,
                            deal_basis=deal_basis,
                            gross_potential=gross_potential,
                            net_potential=net_potential,
                        )
                    )

                    (
                        computed_break_even,
                        computed_total_est_expenses,
                        computed_amount_to_split,
                        computed_walkout_potential,
                    ) = compute_expense_totals(
                        fixed_expenses,
                        variable_expenses,
                        computed_walkout_potential,
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
 
                # ==========================================
                # Expense Breakdown
                # ==========================================

                st.markdown(
                    "##### Expense Breakdown"
                )

                summary_rows = []

                for expense in fixed_rows:

                    if (
                        expense["type"]
                        or expense["amount"] > 0
                    ):

                        summary_rows.append(
                            {
                                "Category": "Fixed",

                                "Expense Type": (
                                    expense["type"]
                                ),

                                "Amount": (
                                    expense["amount"]
                                ),
                            }
                        )

                for expense in variable_rows:

                    if (
                        expense["type"]
                        or expense["amount"] > 0
                    ):

                        summary_rows.append(
                            {
                                "Category": "Variable",

                                "Expense Type": (
                                    expense["type"]
                                ),

                                "Amount": (
                                    expense["amount"]
                                ),
                            }
                        )

                if summary_rows:

                    st.dataframe(

                        summary_rows,

                        use_container_width=True,

                        hide_index=True,

                        column_config={

                            "Amount": (
                                st.column_config.NumberColumn(

                                    "Amount",

                                    format="$%.2f",

                                )
                            ),

                        },

                    )

                else:

                    st.info(
                        "No expenses added."
                    )

            # Store normalized per-show configuration
            show_details.append(
                {
                    "city": show_city,
                    "venue": show_venue,
                    "venue_address": (
                        show_venue_address
                    ),
                    "date": show_date,
                    "schedules": (
                        schedule_rows
                    ),

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

                    # Keep the calculated ticketing-fee values with each show
                    # so the DOCX summary can render the percent and amount.
                    "ticketing_fee_percent": (
                        ticketing_fee_percent
                    ),

                    "ticketing_fee_amount": (
                        ticketing_fee_amount
                    ),

                    "include_merchandising": (
                        include_merchandising
                    ),

                    "merchandising_revenue": (
                        merchandising_revenue
                    ),

                    # Expense breakdown projections
                    "expenses": {

                        # Detailed expense rows
                        "fixed_rows": (
                            fixed_rows
                        ),

                        "variable_rows": (
                            variable_rows
                        ),

                        # Expense totals
                        "fixed_expenses": (
                            fixed_expenses
                        ),

                        "variable_expenses": (
                            variable_expenses
                        ),

                        # Financial calculations
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

    # Return the collected per-show payloads so schedules and show-specific
    # details reach the contract builder instead of falling back to TBD.
    return show_details
