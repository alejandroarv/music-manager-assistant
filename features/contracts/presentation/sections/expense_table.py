# features/contracts/presentation/sections/expense_table.py

# Streamlit UI framework
import streamlit as st

# Expense editor configuration
EXPENSE_TABLE_CONFIG = {

    "fixed": {

        "title": "Fixed Expenses",

        "button": "➕ Add Fixed Expense",

    },

    "variable": {

        "title": "Variable Expenses",

        "button": "➕ Add Variable Expense",

    },

}

def render_expense_table(
    *,
    key_prefix,
    show_index,
    expense_category,
):
    """
    Render a reusable expense editor.

    Responsibilities:
    - Render dynamic expense rows
    - Add expense rows
    - Remove expense rows
    - Calculate expense totals

    Returns:
        tuple[list, float]
            (
                normalized_expense_rows,
                total_expenses,
            )
    """

    config = EXPENSE_TABLE_CONFIG[
        expense_category
    ]

    title = config[
        "title"
    ]

    st.markdown(
        f"##### {title}"
    )

    rows_key = (
        f"{key_prefix}_"
        f"{expense_category}_rows_"
        f"{show_index}"
    )

    if (
        rows_key
        not in st.session_state
    ):

        st.session_state[
            rows_key
        ] = [
            {
                "type": "",
                "amount": 0.0,
            }
        ]

    if st.button(

        config[
            "button"
        ],

        key=(
            f"{key_prefix}"
            f"_add_"
            f"{expense_category}_"
            f"{show_index}"
        ),
    ):

        st.session_state[
            rows_key
        ].append(
            {
                "type": "",
                "amount": 0.0,
            }
        )

    rows = []

    total = 0.0

    for expense_index, _ in enumerate(

        st.session_state[
            rows_key
        ]

    ):
        
        st.caption(
            f"Expense #{expense_index + 1}"
        )

        c1, c2 = st.columns(
            [3, 2]
        )

        with c1:

            expense_type = st.text_input(

                "Expense Type",

                key=(
                    f"{key_prefix}"
                    f"_{expense_category}"
                    f"_type_"
                    f"{show_index}"
                    f"_{expense_index}"
                ),
            )

        with c2:

            amount = st.number_input(

                "Amount",

                min_value=0.0,

                step=100.0,

                value=0.0,

                key=(
                    f"{key_prefix}"
                    f"_{expense_category}"
                    f"_amount_"
                    f"{show_index}"
                    f"_{expense_index}"
                ),
                
            )

        if st.button(

            "Delete Expense",

            key=(

                f"{key_prefix}"

                f"_{expense_category}"

                f"_remove_"

                f"{show_index}"

                f"_{expense_index}"

            ),

        ):

            st.session_state[
                rows_key
            ].pop(
                expense_index
            )

            if not st.session_state[
                rows_key
            ]:

                st.session_state[
                    rows_key
                ] = [
                    {
                        "type": "",
                        "amount": 0.0,
                    }
                ]

            st.rerun()

        rows.append(
            {
                "type": expense_type,
                "amount": amount,
            }
        )

        total += amount

    st.caption(
        f"Total {title}: ${total:,.2f}"
    )

    return rows, total