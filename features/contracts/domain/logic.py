# features/contracts/domain/logic.py

"""
Domain logic for contract document generation.

This module contains pure document-construction logic used
to transform normalized contract data into fully rendered
DOCX and NDA contract outputs.

Responsibilities:
- Template manipulation
- Table replication and population
- Contract field replacement
- Show and ticket formatting
- Document export generation
"""



from io import BytesIO
from copy import deepcopy
from pydoc import doc

from core.models.contracts import (
    NDAContractData,
    PerformanceContractData,
)

from core.templates import get_template

from core.normalizers.contract import (
    normalize_show,
    normalize_performance_contract,
)

from utils.contract_helpers import (
    safe_value,
    format_contract_date,
    parse_date_value,
)

from features.contracts.application.formatters import (
    format_purchaser_term,
)

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

def compute_walkout_potential(
    deal_type: str,
    flat_guarantee: float,
    percentage: float,
    deal_basis: str,
    gross_potential: float,
    net_potential: float,
) -> float:
    """
    Calculate the projected artist walkout
    based on the selected deal structure.
    """

    gross_potential = float(gross_potential or 0)
    net_potential = float(net_potential or 0)
    flat_guarantee = float(flat_guarantee or 0)
    percentage = float(percentage or 0)

    if deal_type == "Flat Guarantee":
        return flat_guarantee

    if deal_type == "Buyout":
        return flat_guarantee

    if deal_type == "Percentage Deal":

        base = (
            net_potential
            if deal_basis == "Net"
            else gross_potential
        )

        return base * (percentage / 100)

    if deal_type == "Versus Deal":

        base = (
            net_potential
            if deal_basis == "Net"
            else gross_potential
        )

        percentage_amount = (
            base * (percentage / 100)
        )

        return max(
            flat_guarantee,
            percentage_amount,
        )

    if deal_type == "Door Deal":

        return (
            gross_potential
            * (percentage / 100)
        )

    return 0.0

def compute_expense_totals(
    fixed_expenses: float,
    variable_expenses: float,
    walkout_potential: float,
) -> tuple[float, float, float, float]:
    """
    Calculate expense and profit projection values.
    """

    total_est_expenses = (
        float(fixed_expenses or 0)
        + float(variable_expenses or 0)
    )

    break_even = total_est_expenses

    walkout_potential = float(
        walkout_potential or 0
    )

    amount_to_split = (
        walkout_potential
        - total_est_expenses
    )

    return (
        break_even,
        total_est_expenses,
        amount_to_split,
        walkout_potential,
    )

def build_performance_fee_clause(
    deal_type: str,
    flat_guarantee: float,
    percentage: float,
    deal_basis: str,
) -> str:
    """
    Build the contract Performance Fee clause
    based on the selected deal structure.
    """

    formatted_guarantee = format_currency(
        flat_guarantee
    )

    formatted_percentage = format_percent(
        percentage
    )

    if deal_type == "Flat Guarantee":

        return (
            f"Flat Guarantee of "
            f"{formatted_guarantee} "
            "NET of any and all "
            "local withholding taxes."
        )

    if deal_type == "Versus Deal":

        return (
            f"The greater of a Minimum "
            f"Guarantee of "
            f"{formatted_guarantee} "
            "NET of any and all local "
            "withholding taxes, or "
            f"{formatted_percentage}% "
            f"of {deal_basis} Box Office "
            "Receipts."
        )

    if deal_type == "Percentage Deal":

        return (
            f"{formatted_percentage}% "
            f"of {deal_basis} Box Office "
            "Receipts, payable NET of "
            "any and all local "
            "withholding taxes."
        )

    if deal_type == "Door Deal":

        return (
            f"{formatted_percentage}% "
            "of Gross Door Receipts, "
            "payable NET of any and all "
            "local withholding taxes."
        )

    if deal_type == "Buyout":

        return (
            f"Buyout Amount of "
            f"{formatted_guarantee} "
            "NET of any and all local "
            "withholding taxes."
        )

    return ""

def build_visa_clause(
    visas_required: bool,
    responsible_party: str,
) -> str:
    """
    Build the Visas / Work Permits clause.
    """

    if visas_required:

        return (
            f"{responsible_party} shall provide and pay "
            "for all necessary visas, work permits, and "
            "documents required for Company, Artist, and "
            "touring party to enter into, perform in, and "
            "depart from the place of the Engagement."
        )

    return (
        "The parties acknowledge that no visas or work "
        "permits are required for the performance(s) "
        "covered by this Agreement. Each party remains "
        "responsible for complying with all applicable "
        "laws and regulations."
    )

def replace_visa_clause(
    doc,
    visas_required,
    responsible_party,
):
    """
    Replace the Visas / Work Permits paragraph
    immediately following its section heading.
    """

    visa_clause = build_visa_clause(
        visas_required,
        responsible_party,
    )

    paragraphs = doc.paragraphs

    for index, paragraph in enumerate(paragraphs):

        if (
            "VISAS/WORK PERMITS"
            in paragraph.text.upper()
        ):

            # The paragraph immediately after the heading
            # contains the legal visa clause.
            if index + 1 < len(paragraphs):

                set_paragraph_text(
                    paragraphs[index + 1],
                    visa_clause,
                )

            return
        
def get_all_tables(doc):
    """
    Retrieve all tables from the document,
    including nested tables.
    """

    tables = list(doc.tables)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:

                # Include nested tables embedded
                # inside parent table cells
                tables.extend(cell.tables)

    return tables


def replace_everywhere(doc, label, value):
    """
    Replace placeholder labels throughout the
    document while preserving surrounding content.
    """

    new_value = f"{label} {value}"

    # Replace placeholders in paragraphs
    for paragraph in doc.paragraphs:

        full_text = "".join(
            run.text for run in paragraph.runs
        )

        if label in full_text:

            before, _, _ = full_text.partition(label)
            new_text = before + new_value

            # Clear existing runs before rebuilding text
            for run in paragraph.runs:
                run.text = ""

            if paragraph.runs:
                paragraph.runs[0].text = new_text

    # Replace placeholders inside tables
    for table in get_all_tables(doc):
        for row in table.rows:
            for cell in row.cells:

                if label in cell.text:

                    before, _, _ = cell.text.partition(label)

                    cell.text = before + new_value

def replace_label_only(
    doc,
    label,
    value,
):
    """
    Replace a label cell entirely with
    the provided value.
    """

    for table in get_all_tables(doc):

        for row in table.rows:

            for cell in row.cells:

                if (
                    cell.text.strip()
                    == label
                ):

                    cell.text = (
                        str(value).strip()
                    )

                    return
                
def replace_performance_fee(
    doc,
    deal_type,
    flat_guarantee,
    percentage,
    deal_basis,
):
    """
    Replace Performance Fee sections
    within contract templates.
    """
    performance_fee_clause = build_performance_fee_clause(
        deal_type,
        flat_guarantee,
        percentage,
        deal_basis,
    )

    for table in get_all_tables(doc):
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:

                    if (
                        "Flat Guarantee of $" in paragraph.text
                        and "NET of any and all local withholding taxes."
                        in paragraph.text
                    ):

                        set_paragraph_text(
                            paragraph,
                            performance_fee_clause,
                        )



def fill_after_header(doc, header_text, value):
    """
    Insert content into the first available
    empty cell following a matching header.
    """

    for table in get_all_tables(doc):
        for row_index, row in enumerate(table.rows):
            for cell in row.cells:

                if header_text in cell.text:

                    for r in range(
                        row_index + 1,
                        len(table.rows)
                    ):

                        for c in table.rows[r].cells:

                            if not c.text.strip():
                                c.text = value
                                return


def fill_merchandising_terms(
    doc,
    merchandising_terms,
):
    """
    Inject merchandising terms into the
    merchandising contract section.
    """

    if not merchandising_terms.strip():
        return

    for table in get_all_tables(doc):

        for row in table.rows:

            for cell in row.cells:

                if (
                    "MERCHANDISING"
                    in cell.text.upper()
                ):

                    # Append terms cleanly
                    cell.text += (
                        "\n\n"
                        "Merchandising Terms:\n"
                        f"{merchandising_terms}"
                    )

                    return


def set_paragraph_text(paragraph, new_text):
    """
    Replace paragraph content while preserving
    paragraph structure.
    """

    # Clear existing run content
    for run in paragraph.runs:
        run.text = ""

    # Rebuild paragraph content
    if paragraph.runs:
        paragraph.runs[0].text = new_text
    else:
        paragraph.add_run(new_text)


def get_show_schedules(show):
    """
    Return non-empty schedule rows from a show.
    """

    rows = (
        show.get("schedules")
        or show.get("schedule")
        or []
    )

    # Drop blank UI rows so an untouched schedule field
    # does not render as an empty "=" line in the contract.
    return [
        row
        for row in rows
        if (
            str(row.get("type", "")).strip()
            or str(row.get("time", "")).strip()
        )
    ]


def format_show_schedule(show):
    """
    Format schedule rows for DOCX templates.
    """

    schedules = get_show_schedules(show)

    if not schedules:
        return "TBD"

    # Keep schedule rendering modular: one row becomes one line,
    # while multiple rows become separate DOCX lines.
    return "\n".join(
        (
            f"{str(item.get('type', '')).strip()} = "
            f"{str(item.get('time', '')).strip()}"
        )
        for item in schedules
    )


def format_effective_date(value):
    """
    Format dates for contract effective date sections.
    """

    parsed = parse_date_value(value)

    if parsed is None:
        return str(value).strip()

    return (
        f"{parsed.strftime('%A, %B')} "
        f"{parsed.day}, {parsed.year}"
    )


def format_header_date(value):
    """
    Format dates for contract header sections.
    """

    parsed = parse_date_value(value)

    if parsed is None:
        return str(value).strip()

    return (
        f"{parsed.strftime('%b')} "
        f"{parsed.day}, {parsed.year}"
    )

def format_short_date(value):
    """
    Format dates using compact MM/DD/YY formatting.
    """

    parsed = parse_date_value(value)

    if parsed is None:
        return str(value).strip()

    return (
        f"{parsed.month}/"
        f"{parsed.day}/"
        f"{parsed.strftime('%y')}"
    )

def update_template_headers(doc, data):
    """
    Update contract header sections using
    normalized contract data.
    """

    header_line = (
        f"{data['artist']} | "
        f"{data['venue']} | "
        f"{data['city']} | "
        f"{format_header_date(data['date'])}"
    )

    single_header_line = (
        f"{data['artist']} | "
        f"{data['venue']} |  | "
        f"{data['city']} | "
        f"{format_header_date(data['date'])}"
    )

    effective_date = format_effective_date(
        data["date"]
    )

    for paragraph in doc.paragraphs:

        text = paragraph.text.strip()

        # Multi-show contract header
        if text == (
            "Artist Name | Venue | City, Country | Date"
        ):

            set_paragraph_text(
                paragraph,
                header_line
            )

        # Single-show contract header
        elif text == (
            "Artist Name | Venue | Festival "
            "(If applicable) |City, Country | Date"
        ):

            set_paragraph_text(
                paragraph,
                single_header_line
            )

        # Update show count section
        elif text == "Number of Shows: TWO (2)":

            set_paragraph_text(
                paragraph,
                "Number of Shows: "
                f"{number_to_words(data['number_of_shows'])} "
                f"({data['number_of_shows']})",
            )

        # Replace template effective date
        elif text == "Thursday, August 17, 2023":

            set_paragraph_text(
                paragraph,
                effective_date
            )

def update_footer(
    doc,
    data,
):
    """
    Update footer placeholders with
    contract information.
    """

    footer_line = (
        f"{data['artist']} | "
        f"{data['venue']} | | "
        f"{data['city']} | "
        f"{format_header_date(data['date'])}"
    )

    for section in doc.sections:

        for paragraph in section.footer.paragraphs:

            text = paragraph.text.strip()

            if (
                "Artist Name" in text
                and "Venue" in text
                and "City, Country" in text
            ):

                set_paragraph_text(
                    paragraph,
                    footer_line,
                )

def number_to_words(value):
    """
    Convert small integer values into uppercase words.
    """

    words = {
        0: "ZERO",
        1: "ONE",
        2: "TWO",
        3: "THREE",
        4: "FOUR",
        5: "FIVE",
        6: "SIX",
        7: "SEVEN",
        8: "EIGHT",
        9: "NINE",
        10: "TEN",
        11: "ELEVEN",
        12: "TWELVE",
    }

    return words.get(value, str(value))


def get_show_tables(doc):
    """
    Retrieve tables associated with
    show detail sections.
    """

    show_tables = []

    for table in get_all_tables(doc):

        cell_texts = [
            cell.text
            for row in table.rows
            for cell in row.cells
        ]

        # Identify show detail tables
        # using known template labels
        if (
            any(
                "City Date:" in text
                for text in cell_texts
            )
            and any(
                "City Venue:" in text
                for text in cell_texts
            )
        ):

            show_tables.append(table)

    return show_tables


def get_body_tables(doc):
    """
    Retrieve top-level document tables.
    """

    return list(doc.tables)


def find_body_tables(doc, predicate):
    """
    Retrieve document tables matching
    a filtering predicate.
    """

    return [
        table
        for table in get_body_tables(doc)
        if predicate(table)
    ]


def find_expense_metric_tables(doc):
    """
    Find visible expense metric tables in document order.
    """

    matches = []

    for table in get_all_tables(doc):

        cell_values = [
            cell.text.strip()
            for row in table.rows
            for cell in row.cells
        ]

        # Use exact cell labels so single-show and multi-show contracts both
        # target the visible TOTAL EXPENSES / DEAL CALCULATIONS table.
        if (
            "Fixed Expenses" in cell_values
            and "Walkout Potential" in cell_values
        ):
            matches.append(table)

    return matches


def get_table_text(table):
    """
    Extract combined text content
    from a table.
    """

    return "\n".join(
        cell.text
        for row in table.rows
        for cell in row.cells
    )


def get_table_text_recursive(table):
    """
    Extract combined text from a table
    and all nested tables.
    """

    return "\n".join(
        get_table_text(current)
        for current in iter_tables_recursive(table)
    )


def is_show_detail_table(table):
    """
    Determine whether a table represents
    a show detail section.
    """

    nested_text = get_table_text_recursive(table)

    return (
        "City Date:" in nested_text
        and "City Venue:" in nested_text
    )


def is_ticket_pricing_table(table):
    """
    Determine whether a table represents
    ticket pricing information.
    """

    try:
        return (
            table.rows[0]
            .cells[0]
            .text.strip()
            == "City - Venue - Date"
        )

    except IndexError:
        return False


def is_ticket_summary_table(table):
    """
    Determine whether a table represents
    ticket summary information.
    """

    text = get_table_text_recursive(table)

    return (
        "Gross Potential" in text
        and "Net Potential" in text
    )


def is_expense_table(table):
    """
    Determine whether a table represents
    an expense breakdown section.
    """

    text = get_table_text_recursive(table)

    return (
        # Single-show templates use "EXPENSES" while multi-show templates use
        # "EXPENSES for ...", so match the shared heading plus a metric label.
        "EXPENSES" in text
        and "Walkout Potential" in text
    )


def insert_table_after(table, template_table):
    """
    Duplicate and insert a table directly
    after another table.
    """

    new_tbl = deepcopy(template_table._tbl)

    table._tbl.addnext(new_tbl)

    return table.__class__(
        new_tbl,
        table._parent
    )


def ensure_repeated_tables(
    doc,
    number_of_shows
):
    """
    Dynamically replicate template table sections
    for multi-show performance contracts.

    Ensures the document contains enough repeated
    structures to render all configured shows.
    """

    show_detail_tables = find_body_tables(
        doc,
        is_show_detail_table
    )

    ticket_pricing_tables = find_body_tables(
        doc,
        is_ticket_pricing_table
    )

    ticket_summary_tables = find_body_tables(
        doc,
        is_ticket_summary_table
    )

    expense_tables = find_expense_metric_tables(
        doc
    )

    # Abort if required template sections
    # are missing from the document
    if not (
        show_detail_tables
        and ticket_pricing_tables
        and ticket_summary_tables
        and expense_tables
    ):
        return

    # Use the final template sections
    # as duplication sources
    show_template = deepcopy(
        show_detail_tables[-1]._tbl
    )

    ticket_template = deepcopy(
        ticket_pricing_tables[-1]._tbl
    )

    summary_template = deepcopy(
        ticket_summary_tables[-1]._tbl
    )

    expense_template = deepcopy(
        expense_tables[-1]._tbl
    )

    # Replicate show detail sections
    while len(show_detail_tables) < number_of_shows:

        new_tbl = deepcopy(show_template)

        show_detail_tables[-1]._tbl.addnext(
            new_tbl
        )

        show_detail_tables.append(
            show_detail_tables[-1].__class__(
                new_tbl,
                show_detail_tables[-1]._parent
            )
        )

    # Replicate ticket pricing and
    # summary sections together
    while (
        len(ticket_pricing_tables)
        < number_of_shows
    ):

        new_ticket_tbl = deepcopy(
            ticket_template
        )

        ticket_summary_tables[-1]._tbl.addnext(
            new_ticket_tbl
        )

        new_ticket = (
            ticket_pricing_tables[-1].__class__(
                new_ticket_tbl,
                ticket_summary_tables[-1]._parent
            )
        )

        ticket_pricing_tables.append(
            new_ticket
        )

        new_summary_tbl = deepcopy(
            summary_template
        )

        new_ticket._tbl.addnext(
            new_summary_tbl
        )

        ticket_summary_tables.append(
            new_ticket.__class__(
                new_summary_tbl,
                new_ticket._parent
            )
        )

    # Replicate expense sections
    while len(expense_tables) < number_of_shows:

        new_tbl = deepcopy(expense_template)

        expense_tables[-1]._tbl.addnext(
            new_tbl
        )

        expense_tables.append(
            expense_tables[-1].__class__(
                new_tbl,
                expense_tables[-1]._parent
            )
        )


def iter_tables_recursive(table):
    """
    Recursively iterate through nested DOCX tables.
    """

    yield table

    for row in table.rows:
        for cell in row.cells:
            for nested_table in cell.tables:

                yield from iter_tables_recursive(
                    nested_table
                )


def iter_table_cells_recursive(table):
    """
    Recursively iterate through all cells in
    a table, including nested table cells.
    """

    for current_table in iter_tables_recursive(table):
        for row in current_table.rows:
            for cell in row.cells:
                yield cell


def replace_text_in_cell(cell, replacements):
    """
    Replace placeholder text inside a table
    cell while preserving paragraph structure.
    """

    for paragraph in cell.paragraphs:

        full_text = "".join(
            run.text
            for run in paragraph.runs
        )

        if not full_text:
            continue

        new_text = full_text

        # Apply all signature placeholders that may appear in
        # either the nested purchaser side or visible company side.
        for target, value in replacements.items():
            new_text = new_text.replace(
                target,
                str(value)
            )

        if new_text == full_text:
            continue

        set_paragraph_text(
            paragraph,
            new_text
        )


def fill_show_table(
    table,
    show,
    show_length
):
    """
    Populate a show detail table using
    normalized show information.
    """

    city_label = (
        show["city"]
        .strip()
    )

    for current_table in iter_tables_recursive(table):

        for row in current_table.rows:
            for cell in row.cells:

                text = cell.text

                # Replace show-specific placeholders
                if "City Date:" in text:

                    weekday = (
                        show["raw_date"]
                        .strftime("%A")
                    )

                    cell.text = (
                        f"{city_label} Date: "
                        f"{weekday}, "
                        f"{show['date']}"
                    )

                elif "City Venue:" in text:

                    cell.text = (
                        f"{city_label} Venue: "
                        f"{show['venue']}"
                    )

                elif "City Schedule:" in text:

                    cell.text = (
                        f"{city_label} Schedule:\n"
                        f"{format_show_schedule(show)}"
                    )

                elif "City Length:" in text:

                    cell.text = (
                        f"{city_label} Length: "
                        f"{show_length}"
                    )

                elif "City Capacity:" in text:

                    cell.text = (
                        f"{city_label} Capacity: "
                        f"{show['capacity']}"
                    )

                elif "City  Additional Acts:" in text:

                    cell.text = (
                        f"{city_label} Additional Acts: "
                        f"{show['additional_acts']}"
                    )



def format_currency(value):
    """
    Format numeric values as standardized
    currency strings.
    """

    try:
        return f"$ {float(value):,.0f}"

    except (TypeError, ValueError):

        return (
            str(value).strip()
            or "$ 0.00"
        )


def format_percent(value):
    """
    Format percentages without unnecessary
    trailing decimal places.
    """

    try:
        numeric_value = float(value)

    except (TypeError, ValueError):
        return str(value).strip() or "0"

    if numeric_value.is_integer():
        return str(int(numeric_value))

    return f"{numeric_value:g}"


def fill_ticketing_fee_paragraph(cell, ticketing_fee_text):
    """
    Fill the ticketing-fee value without disturbing
    the nested gross/net potential table.
    """

    paragraphs = list(cell.paragraphs)

    for paragraph in paragraphs:

        if paragraph.text.strip() != "Ticketing Fees":
            continue

        # The label is italic and sits in the outer cell, while gross/net live
        # in a nested table. Appending the value to the label paragraph keeps it
        # visible without rewriting the nested gross/net potential rows.
        paragraph.add_run(
            f"\n{ticketing_fee_text}"
        )

        return True

    return False


def fill_ticket_pricing_table(table, show):
    """
    Populate ticket pricing tables using
    normalized show ticket data.
    """

    header_value = (
        f"{show['city']} - "
        f"{show['venue']} - "
        f"{show['date']}"
    ).strip(" -")

    table.rows[0].cells[0].text = (
        header_value
    )

    rows = show.get("ticket_rows", [])

    # Populate pricing rows
    for row_index, row_data in enumerate(
        rows,
        start=1
    ):

        if row_index >= len(table.rows):
            break

        row = table.rows[row_index]

        row.cells[0].text = str(
            row_data.get(
                "label",
                row.cells[0].text
            )
        )

        row.cells[1].text = str(
            row_data.get("total", "")
        )

        row.cells[2].text = str(
            row_data.get(
                "comps_kills",
                ""
            )
        )

        row.cells[3].text = format_currency(
            row_data.get("price", 0)
        )

        row.cells[4].text = format_currency(
            row_data.get(
                "line_total",
                0
            )
        )

    # Populate aggregate totals
    if len(table.rows) > 1:

        total_row = table.rows[-1]

        total_row.cells[1].text = str(
            show.get("ticket_total", "")
        )

        total_row.cells[2].text = str(
            show.get(
                "ticket_comps_kills",
                ""
            )
        )


def fill_ticket_summary_table(table, show):
    """
    Populate ticket summary sections with
    gross and net revenue projections.
    """

    gross = show.get(
        "gross_potential",
        0
    )

    net = show.get(
        "net_potential",
        0
    )

    ticketing_fee_percent = (
        show.get(
            "ticketing_fee_percent",
            0
        )
    )

    ticketing_fee_amount = (
        show.get(
            "ticketing_fee_amount",
            0
        )
    )

    ticketing_fee_text = (
        f"{format_percent(ticketing_fee_percent)}% "
        f"({format_currency(ticketing_fee_amount)})"
    )

    for cell in table.rows[0].cells:
        fill_ticketing_fee_paragraph(
            cell,
            ticketing_fee_text,
        )

    for nested in (
        table.rows[0]
        .cells[0]
        .tables
    ):

        # Keep gross/net updates scoped to the nested table cells so the
        # outer ticketing-fee paragraph does not wipe those existing rows.
        nested.rows[0].cells[4].text = (
            format_currency(gross)
        )

        nested.rows[1].cells[4].text = (
            format_currency(net)
        )


def set_table_value_after_label(table, label, value):
    """
    Fill the value cell that follows a label
    in DOCX tables that contain spacer cells.
    """

    for row in table.rows:

        cells = list(row.cells)

        for index, cell in enumerate(cells):

            if cell.text.strip() != label:
                continue

            target_index = min(
                index + 2,
                len(cells) - 1,
            )

            # Expense rows use blank spacer cells between labels and values,
            # so the value usually sits two cells after the matching label.
            cells[target_index].text = value

            return True

    return False


def fill_expense_table(table, show):
    """
    Populate expense breakdown tables using
    normalized financial projections.
    """

    expenses = show.get("expenses", {})

    # Fill by label instead of fixed row/column indexes because the single
    # and multi templates use spacer/merged cells differently.
    set_table_value_after_label(
        table,
        "Fixed Expenses",
        format_currency(
            expenses.get("fixed_expenses", 0)
        ),
    )

    set_table_value_after_label(
        table,
        "Net Potential",
        format_currency(
            expenses.get("net_potential", 0)
        ),
    )

    set_table_value_after_label(
        table,
        "Variable Expenses",
        format_currency(
            expenses.get("variable_expenses", 0)
        ),
    )

    set_table_value_after_label(
        table,
        "Total Est. Expenses",
        format_currency(
            expenses.get("total_est_expenses", 0)
        ),
    )

    set_table_value_after_label(
        table,
        "Break Even",
        format_currency(
            expenses.get("break_even", 0)
        ),
    )

    set_table_value_after_label(
        table,
        "Amount to Split",
        format_currency(
            expenses.get("amount_to_split", 0)
        ),
    )

    set_table_value_after_label(
        table,
        "Walkout Potential",
        format_currency(
            expenses.get("walkout_potential", 0)
        ),
    )


def update_performance_fee_table(
    doc,
    shows,
    deal_type,
    flat_guarantee,
    percentage,
    deal_basis,
):
    """
    Update multi-show Performance Fee sections
    across contract payment tables.
    """

    performance_fee_clause = build_performance_fee_clause(
        deal_type,
        flat_guarantee,
        percentage,
        deal_basis,
    )

    for table in get_body_tables(doc):

        if (
            "NET of any and all local "
            "withholding taxes."
            not in get_table_text(table)
        ):
            continue

        cell = table.rows[0].cells[0]

        if not cell.paragraphs:
            return

        # Update primary guarantee section
        set_paragraph_text(
            cell.paragraphs[0],
            performance_fee_clause,
        )

        # Retrieve existing event paragraphs
        event_paragraphs = [
            p
            for p in cell.paragraphs[2:]
            if p.text.strip()
        ]

        # Dynamically add paragraphs for
        # additional shows if needed
        while len(event_paragraphs) < len(shows):

            event_paragraphs.append(
                cell.add_paragraph()
            )

        # Populate show-specific guarantees
        for index, show in enumerate(shows):

            if deal_type == "Flat Guarantee":

                line = (
                    f"Flat Guarantee of "
                    f"{format_currency(flat_guarantee)} "
                    f"for the event on "
                    f"{show.get('date', '')}"
                )

            elif deal_type == "Buyout":

                line = (
                    f"Buyout Amount of "
                    f"{format_currency(flat_guarantee)} "
                    f"for the event on "
                    f"{show.get('date', '')}"
                )

            elif deal_type == "Versus Deal":

                line = (
                    f"Versus Deal for the event on "
                    f"{show.get('date', '')}"
                )

            elif deal_type == "Percentage Deal":

                line = (
                    f"{format_percent(percentage)}% "
                    f"of {deal_basis} Box Office "
                    f"Receipts for the event on "
                    f"{show.get('date', '')}"
                )

            elif deal_type == "Door Deal":

                line = (
                    f"{format_percent(percentage)}% "
                    f"of Gross Door Receipts "
                    f"for the event on "
                    f"{show.get('date', '')}"
                )

            else:

                line = ""

            set_paragraph_text(
                event_paragraphs[index],
                line,
            )

        # Clear unused template paragraphs
        for extra in event_paragraphs[len(shows):]:

            set_paragraph_text(extra, "")

        return


def update_show_related_tables(
    doc,
    shows,
    deal_type,
    flat_guarantee,
    percentage,
    deal_basis,
):
    """
    Update all show-related financial
    and ticketing sections.
    """

    ticket_tables = find_body_tables(
        doc,
        is_ticket_pricing_table
    )

    ticket_summary_tables = find_body_tables(
        doc,
        is_ticket_summary_table
    )

    expense_tables = find_expense_metric_tables(
        doc
    )

    # Populate financial sections
    # for each configured show
    for index, show in enumerate(shows):

        if index < len(ticket_tables):

            fill_ticket_pricing_table(
                ticket_tables[index],
                show
            )

        if index < len(ticket_summary_tables):

            fill_ticket_summary_table(
                ticket_summary_tables[index],
                show
            )

        if index < len(expense_tables):

            fill_expense_table(
                expense_tables[index],
                show
            )

    # Multi-show contracts require
    # expanded payment breakdown sections
    if len(shows) > 1:

        update_performance_fee_table(
            doc,
            shows,
            deal_type,
            flat_guarantee,
            percentage,
            deal_basis,
        )

def fill_single_show_details(doc, show):
    """
    Populate single-show contract sections
    using normalized show data.
    """

    for table in get_body_tables(doc):

        text = get_table_text(table)

        # Populate single-show details section
        if (
            "DATE OF SHOW(S):" in text
            and "SCHEDULE" in text
        ):

            weekday = (
                show["raw_date"]
                .strftime("%A")
            )

            table.rows[0].cells[0].text = (
                f"DATE OF SHOW(S): "
                f"{weekday}, "
                f"{show['date']}"
            )

            table.rows[1].cells[0].text = (
                "NUMBER OF SHOW(S): 1"
            )

            table.rows[2].cells[0].text = (
                f"SHOW LENGTH: "
                f"{show['show_length']}"
            )

            table.rows[3].cells[0].text = (
                "ADDITIONAL ACTS: "
                f"{show['additional_acts']}"
            )

            table.rows[4].cells[0].text = (
                f"CAPACITY: "
                f"{show['capacity']}"
            )

            # The single-show template has its own SCHEDULE row,
            # so write the modular schedule text directly there.
            table.rows[5].cells[0].text = (
                "SCHEDULE:\n"
                f"{format_show_schedule(show)}"
            )

        # Populate venue information section
        elif (
            "VENUE:" in text
            and "Address:" in text
        ):

            table.rows[0].cells[0].text = (
                f"VENUE: "
                f"{show['venue']}"
            )

            table.rows[1].cells[0].text = (
                f"Address: "
                f"{show['venue_address']}"
            )


def replace_nth_occurrence(
    doc,
    label,
    value,
    occurrence_index
):
    """
    Replace a specific occurrence of a label
    within the document.
    """

    count = 0

    # Search paragraphs first
    for paragraph in doc.paragraphs:

        full_text = "".join(
            run.text
            for run in paragraph.runs
        )

        if label in full_text:

            if count == occurrence_index:

                before, _, _ = (
                    full_text.partition(label)
                )

                new_text = (
                    before
                    + f"{label} {value}"
                )

                for run in paragraph.runs:
                    run.text = ""

                if paragraph.runs:
                    paragraph.runs[0].text = (
                        new_text
                    )

                return

            count += 1

    # Search tables after paragraphs
    for table in get_all_tables(doc):
        for row in table.rows:
            for cell in row.cells:

                if label in cell.text:

                    if count == occurrence_index:

                        before, _, _ = (
                            cell.text.partition(label)
                        )

                        cell.text = (
                            before
                            + f"{label} {value}"
                        )

                        return

                    count += 1


def replace_schedule_preserve_format(
    doc,
    show,
    value,
    occurrence_index
):
    """
    Inject schedule values while preserving
    existing DOCX run formatting.
    """

    count = 0

    def normalize(text):
        """
        Normalize text for resilient
        placeholder matching.
        """

        return (
            text.lower()
            .replace(" ", "")
        )

    for table in get_all_tables(doc):
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:

                    runs = paragraph.runs

                    if not runs:
                        continue

                    full_text = "".join(
                        run.text for run in runs
                    )

                    normalized_text = normalize(
                        full_text
                    )

                    if (
                        "cityschedule:"
                        in normalized_text
                        or "schedule:"
                        in normalized_text
                    ):

                        if count == occurrence_index:

                            set_paragraph_text(
                                paragraph,
                                (
                                    f"{show.get('city', 'City')} "
                                    "Schedule:\n"
                                    f"{value}"
                                ),
                            )
                            return

                        count += 1


def fill_show_sections(doc, shows):
    """
    Populate all show detail sections
    within the contract template.
    """

    show_tables = get_show_tables(doc)

    for index, show in enumerate(shows):

        if index >= len(show_tables):
            break

        fill_show_table(
            show_tables[index],
            show,
            show["show_length"],
        )
        replace_schedule_preserve_format(
            doc,
            show,
            format_show_schedule(show),
            index,
        )

def fill_signature_table(doc, data):
    """
    Populate signature and buyer information
    sections within the contract template.
    """

    replacements = {
        "[sig|req|signer1]": "[sig|req|signer1]",
        "Buyer Name": data["buyer_name"],
        "Buyer Company Name": data["buyer_company_name"],
        "Buyer Company": data["buyer_company_name"],
        "[date|date|signer1]": format_header_date(
            data["signature_date"]
        ),
        "Manager Name": data["manager_name"],
        "Manager Company Name": data["manager_company_name"],
    }

    for table in get_body_tables(doc):

        table_text = get_table_text_recursive(table)

        if not (
            "PURCHASER" in table_text
            and "COMPANY" in table_text
            and (
                "Buyer Name" in table_text
                or "Manager Name" in table_text
            )
        ):
            continue

        # Replace signature-related placeholders across both
        # the nested purchaser table and the outer company cell.
        for cell in iter_table_cells_recursive(table):
            replace_text_in_cell(
                cell,
                replacements
            )

        return


def build_performance_contract(
    data: PerformanceContractData
) -> bytes:
    """
    Generate a fully rendered performance
    contract document.

    Responsibilities:
    - Load the appropriate template
    - Normalize contract data
    - Populate placeholders and tables
    - Render show-related financial sections
    - Export the document as DOCX bytes
    """

    template_name = (
        "performance_single"
        if data.number_of_shows == 1
        else "performance_multi"
    )

    # Load DOCX contract template
    doc = get_template(
        template_name
    )

    # Normalize contract data before rendering
    normalized = normalize_performance_contract(
        data
    )

    # Dynamically replicate template sections
    # for contracts containing many shows
    if data.number_of_shows > 2:

        ensure_repeated_tables(
            doc,
            data.number_of_shows
        )

    # Populate shared contract sections
    replace_performance_fee(
        doc,
        normalized["deal_type"],
        normalized["flat_guarantee"],
        normalized["percentage"],
        normalized["deal_basis"],
    )

    update_template_headers(
        doc,
        normalized
    )

    update_footer(
        doc,
        normalized,
    )

    replace_everywhere(
        doc,
        "PURCHASER NAME:",
        normalized["purchaser_name"]
    )

    replace_nth_occurrence(
        doc,
        "Address:",
        normalized["purchaser_address"],
        0
    )

    replace_everywhere(
        doc,
        "Signatory:",
        normalized["signatory"]
    )

    replace_everywhere(
        doc,
        "COMPANY NAME:",
        normalized["company_name"]
    )

    replace_nth_occurrence(
        doc,
        "Address:",
        normalized["company_address"],
        1
    )

    replace_everywhere(
        doc,
        "VENUE:",
        normalized["venue"]
    )

    replace_everywhere(
        doc,
        "DATE OF SHOW(S):",
        format_contract_date(
            normalized["date"]
        )
    )

    replace_everywhere(
        doc,
        "Company is furnishing "
        "the services of",
        normalized["artist"],
    )

    replace_everywhere(
        doc,
        "NUMBER OF SHOW(S):",
        str(normalized["number_of_shows"])
    )

    replace_everywhere(
        doc,
        "SHOW LENGTH:",
        normalized["show_length"]
    )

    replace_everywhere(
        doc,
        "ADDITIONAL ACTS:",
        normalized["additional_acts"]
    )

    # Travel and logistics sections
    replace_everywhere(
        doc,
        "Air Transportation:",
        format_purchaser_term(
            normalized["purchaser_name"],

            "Air Transportation",

            normalized["air_transportation"],
        )
    )

    replace_everywhere(
        doc,
        "Hotel Accommodations:",
        format_purchaser_term(
            normalized["purchaser_name"],

            "Hotel Accommodations",

            normalized[
                "hotel_accommodations"
            ],
        )
    )

    replace_everywhere(
        doc,
        "Air Freight & Excess Baggage:",
        format_purchaser_term(
            normalized["purchaser_name"],

            "Air Freight & Excess Baggage",

            normalized[
                "air_freight"
            ],
        )
    )

    replace_everywhere(
        doc,
        "Ground Transportation:",
        format_purchaser_term(
            normalized["purchaser_name"],

            "Ground Transportation",

            normalized[
                "ground_transportation"
            ],
        )
    )

    replace_everywhere(
        doc,
        "Meals & Incidentals:",
        format_purchaser_term(
            normalized["purchaser_name"],

            "Meals & Incidentals",

            normalized[
                "meals_incidentals"
            ],
        )
    )

    replace_visa_clause(
        doc,
        normalized["visas_required"],
        (
            normalized["purchaser_name"]
            if normalized["visa_responsible_party"] == "Purchaser"
            else normalized["company_name"]
        ),
    )

    replace_visa_clause(
        doc,
        normalized["visas_required"],
        (
            normalized["purchaser_name"]
            if normalized["visa_responsible_party"] == "Purchaser"
            else normalized["company_name"]
        ),
    )

    # Contract and merchandising terms
    replace_label_only(
        doc,
        "Special Provisions:",
        normalized["special_provisions"]
    )

    replace_everywhere(
        doc,
        "Concessionaire fee:",
        normalized["concessionaire_fee"]
    )

    replace_everywhere(
        doc,
        "Seller:",
        normalized["seller"]
    )

    replace_everywhere(
        doc,
        "Hard Merchandising:",
        normalized["hard_merchandising"]
    )

    replace_everywhere(
        doc,
        "Soft Merchandising:",
        normalized["soft_merchandising"]
    )

    replace_label_only(
        doc,
        "Complimentary Tickets:",
        normalized["complimentary_tickets"]
    )

    replace_exact_text(
        doc,
        "Artist Name - 100% Headliner",
        f"{normalized['artist']} - 100% Headliner",
    )

    # Populate large free-text sections
    replace_label_only(
        doc,
        "Production:",
        normalized["production"]
    )

    replace_label_only(
        doc,
        "Catering:",
        normalized["catering"]
    )

    replace_label_only(
        doc,
        "Additional Addenda:",
        normalized["additional_addenda"]
    )

    fill_merchandising_terms(
        doc,
        normalized["merchandising_terms"]
    )

    # Populate signature sections
    fill_signature_table(
        doc,
        normalized
    )

    replace_label_only(
        doc,
        "Buyer Company",
        normalized["buyer_name"]
    )

    replace_label_only(
        doc,
        "Buyer Company Name",
        normalized["buyer_company_name"]
    )

    replace_label_only(
        doc,
        "Manager Name",
        normalized["manager_name"]
    )

    replace_label_only(
        doc,
        "Manager Company Name",
        normalized["manager_company_name"]
    )

    # Build fallback single-show structure
    # when explicit show data is absent
    raw_shows = normalized["shows"] or [
        {
            "date": normalized["date"],
            "venue": normalized["venue"],
            "venue_address": normalized["venue_address"],
            "time": "",
            "notes": normalized["additional_acts"],
            "capacity": "",
            "show_length": normalized["show_length"],
            "city": normalized["city"],
        }
    ]

    # Normalize individual show entries
    normalized_shows = [
        normalize_show(show, normalized)
        for show in raw_shows
    ]

    # Populate show sections depending
    # on contract configuration
    if data.number_of_shows > 1:

        fill_show_sections(
            doc,
            normalized_shows
        )

    else:

        fill_single_show_details(
            doc,
            normalized_shows[0]
        )

    # Populate ticketing and financial sections
    update_show_related_tables(
        doc,
        normalized_shows[
            : data.number_of_shows
        ],
        normalized["deal_type"],
        normalized["flat_guarantee"],
        normalized["percentage"],
        normalized["deal_basis"],
    )

    # Export final DOCX document
    buffer = BytesIO()

    doc.save(buffer)

    buffer.seek(0)

    return buffer.getvalue()

def replace_exact_text(
    doc,
    target,
    replacement,
):
    """
    Replace an entire cell or paragraph
    when its text exactly matches the target.
    """

    for paragraph in doc.paragraphs:

        if paragraph.text.strip() == target:

            set_paragraph_text(
                paragraph,
                replacement,
            )

    for table in get_all_tables(doc):

        for row in table.rows:

            for cell in row.cells:

                if (
                    cell.text.strip()
                    == target
                ):

                    cell.text = replacement

def build_nda_contract(
    data: NDAContractData,
    template: str
):
    """
    Generate an NDA contract using
    a text-based template.
    """

    return template.format(
        disclosing_party=data.disclosing_party,
        receiving_party=data.receiving_party,
        purpose=data.purpose,
        duration=data.duration,
    )
