# features/contracts/domain/logic.py

from io import BytesIO
from copy import deepcopy

from core.models.contracts import NDAContractData, PerformanceContractData
from core.templates import get_template

from core.normalizers.contract import normalize_show

from utils.contract_helpers import (
    safe_value,
    format_contract_date,
    parse_date_value,
)
from core.normalizers.contract import normalize_performance_contract

def get_all_tables(doc):
    tables = list(doc.tables)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                tables.extend(cell.tables)
    return tables


def replace_everywhere(doc, label, value):
    new_value = f"{label} {value}"

    for paragraph in doc.paragraphs:
        full_text = "".join(run.text for run in paragraph.runs)

        if label in full_text:
            before, _, _ = full_text.partition(label)
            new_text = before + new_value

            for run in paragraph.runs:
                run.text = ""

            if paragraph.runs:
                paragraph.runs[0].text = new_text

    for table in get_all_tables(doc):
        for row in table.rows:
            for cell in row.cells:
                if label in cell.text:
                    before, _, _ = cell.text.partition(label)
                    cell.text = before + new_value


def replace_fee(doc, formatted_fee):
    for table in get_all_tables(doc):
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    if (
                        "Flat Guarantee of $" in paragraph.text
                        and "NET of any and all local withholding taxes." in paragraph.text
                    ):
                        set_paragraph_text(
                            paragraph,
                            f"Flat Guarantee of $ {formatted_fee} NET of any and all "
                            "local withholding taxes.",
                        )


def fill_after_header(doc, header_text, value):
    for table in get_all_tables(doc):
        for row_index, row in enumerate(table.rows):
            for cell in row.cells:
                if header_text in cell.text:
                    for r in range(row_index + 1, len(table.rows)):
                        for c in table.rows[r].cells:
                            if not c.text.strip():
                                c.text = value
                                return


def set_paragraph_text(paragraph, new_text):
    for run in paragraph.runs:
        run.text = ""

    if paragraph.runs:
        paragraph.runs[0].text = new_text
    else:
        paragraph.add_run(new_text)


def format_effective_date(value):
    parsed = parse_date_value(value)
    if parsed is None:
        return str(value).strip()

    return f"{parsed.strftime('%A, %B')} {parsed.day}, {parsed.year}"


def format_header_date(value):
    parsed = parse_date_value(value)
    if parsed is None:
        return str(value).strip()

    return f"{parsed.strftime('%b')} {parsed.day}, {parsed.year}"


def format_short_date(value):
    parsed = parse_date_value(value)
    if parsed is None:
        return str(value).strip()

    return f"{parsed.month}/{parsed.day}/{parsed.strftime('%y')}"



def update_template_headers(doc, data):
    header_line = f"{data['artist']} | {data['venue']} | {data['city']} | {format_header_date(data['date'])}"
    single_header_line = (
        f"{data['artist']} | {data['venue']} |  | {data['city']} | {format_header_date(data['date'])}"
    )
    effective_date = format_effective_date(data["date"])

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()

        if text == "Artist Name | Venue | City, Country | Date":
            set_paragraph_text(paragraph, header_line)
        elif text == "Artist Name | Venue | Festival (If applicable) |City, Country | Date":
            set_paragraph_text(paragraph, single_header_line)
        elif text == "Number of Shows: TWO (2)":
            set_paragraph_text(
                paragraph,
                f"Number of Shows: {number_to_words(data['number_of_shows'])} ({data['number_of_shows']})",
            )
        elif text == "Thursday, August 17, 2023":
            set_paragraph_text(paragraph, effective_date)


def number_to_words(value):
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
    show_tables = []

    for table in get_all_tables(doc):
        cell_texts = [cell.text for row in table.rows for cell in row.cells]
        if any("City Date:" in text for text in cell_texts) and any(
            "City Venue:" in text for text in cell_texts
        ):
            show_tables.append(table)

    return show_tables


def get_body_tables(doc):
    return list(doc.tables)


def find_body_tables(doc, predicate):
    return [table for table in get_body_tables(doc) if predicate(table)]


def get_table_text(table):
    return "\n".join(cell.text for row in table.rows for cell in row.cells)


def get_table_text_recursive(table):
    return "\n".join(get_table_text(current) for current in iter_tables_recursive(table))


def is_show_detail_table(table):
    nested_text = get_table_text_recursive(table)
    return "City Date:" in nested_text and "City Venue:" in nested_text


def is_ticket_pricing_table(table):
    try:
        return table.rows[0].cells[0].text.strip() == "City - Venue - Date"
    except IndexError:
        return False


def is_ticket_summary_table(table):
    text = get_table_text_recursive(table)
    return "Gross Potential" in text and "Net Potential" in text


def is_expense_table(table):
    text = get_table_text_recursive(table)
    return "EXPENSES for " in text and "Walkout Potential" in text


def insert_table_after(table, template_table):
    new_tbl = deepcopy(template_table._tbl)
    table._tbl.addnext(new_tbl)
    return table.__class__(new_tbl, table._parent)


def ensure_repeated_tables(doc, number_of_shows):
    show_detail_tables = find_body_tables(doc, is_show_detail_table)
    ticket_pricing_tables = find_body_tables(doc, is_ticket_pricing_table)
    ticket_summary_tables = find_body_tables(doc, is_ticket_summary_table)
    expense_tables = find_body_tables(doc, is_expense_table)

    if not (
        show_detail_tables
        and ticket_pricing_tables
        and ticket_summary_tables
        and expense_tables
    ):
        return

    show_template = deepcopy(show_detail_tables[-1]._tbl)
    ticket_template = deepcopy(ticket_pricing_tables[-1]._tbl)
    summary_template = deepcopy(ticket_summary_tables[-1]._tbl)
    expense_template = deepcopy(expense_tables[-1]._tbl)

    while len(show_detail_tables) < number_of_shows:
        new_tbl = deepcopy(show_template)
        show_detail_tables[-1]._tbl.addnext(new_tbl)
        show_detail_tables.append(show_detail_tables[-1].__class__(new_tbl, show_detail_tables[-1]._parent))

    while len(ticket_pricing_tables) < number_of_shows:
        new_ticket_tbl = deepcopy(ticket_template)
        ticket_summary_tables[-1]._tbl.addnext(new_ticket_tbl)
        new_ticket = ticket_pricing_tables[-1].__class__(new_ticket_tbl, ticket_summary_tables[-1]._parent)
        ticket_pricing_tables.append(new_ticket)

        new_summary_tbl = deepcopy(summary_template)
        new_ticket._tbl.addnext(new_summary_tbl)
        ticket_summary_tables.append(new_ticket.__class__(new_summary_tbl, new_ticket._parent))

    while len(expense_tables) < number_of_shows:
        new_tbl = deepcopy(expense_template)
        expense_tables[-1]._tbl.addnext(new_tbl)
        expense_tables.append(expense_tables[-1].__class__(new_tbl, expense_tables[-1]._parent))


def iter_tables_recursive(table):
    yield table

    for row in table.rows:
        for cell in row.cells:
            for nested_table in cell.tables:
                yield from iter_tables_recursive(nested_table)


def fill_show_table(table, show, show_length, capacity, notes):
    for current_table in iter_tables_recursive(table):
        for row in current_table.rows:
            for cell in row.cells:
                text = cell.text

                if "City Date:" in text:
                    cell.text = f"City Date: {show['date']}"
                elif "City Venue:" in text:
                    cell.text = f"City Venue: {show['venue']}"
                elif "City Length:" in text:
                    cell.text = f"City Length: {show_length}"
                elif "City Capacity:" in text:
                    cell.text = f"City Capacity: {show['capacity']}"
                elif "City  Additional Acts:" in text:
                    cell.text = f"City  Additional Acts: {show['additional_acts']}"
                elif "City Schedule:" in text or "City  Schedule:" in text:
                    cell.text = f"City Schedule: {show['time']}"


def format_currency(value):
    try:
        return f"$ {float(value):,.2f}"
    except (TypeError, ValueError):
        return str(value).strip() or "$ 0.00"


def fill_ticket_pricing_table(table, show):
    header_value = f"{show['city']} - {show['venue']} - {show['date']}".strip(" -")
    table.rows[0].cells[0].text = header_value

    rows = show.get("ticket_rows", [])
    for row_index, row_data in enumerate(rows, start=1):
        if row_index >= len(table.rows):
            break
        row = table.rows[row_index]
        row.cells[0].text = str(row_data.get("label", row.cells[0].text))
        row.cells[1].text = str(row_data.get("total", ""))
        row.cells[2].text = str(row_data.get("comps_kills", ""))
        row.cells[3].text = format_currency(row_data.get("price", 0))
        row.cells[4].text = format_currency(row_data.get("line_total", 0))

    if len(table.rows) > 1:
        total_row = table.rows[-1]
        total_row.cells[1].text = str(show.get("ticket_total", ""))
        total_row.cells[2].text = str(show.get("ticket_comps_kills", ""))


def fill_ticket_summary_table(table, show):
    gross = show.get("gross_potential", 0)
    net = show.get("net_potential", 0)

    for nested in table.rows[0].cells[0].tables:
        nested.rows[0].cells[4].text = format_currency(gross)
        nested.rows[1].cells[4].text = format_currency(net)


def fill_expense_table(table, show):
    title = (
        f"EXPENSES for {show['city']} - {show['venue']} - "
        f"{format_short_date(show.get('raw_date', show['date']))}"
    ).strip()
    expenses = show.get("expenses", {})

    if table.rows and table.rows[0].cells and table.rows[0].cells[0].tables:
        table.rows[0].cells[0].tables[0].rows[0].cells[0].text = title

    if table.rows and table.rows[0].cells and len(table.rows[0].cells[0].tables) > 1:
        nested = table.rows[0].cells[0].tables[1]
        nested.rows[1].cells[2].text = format_currency(expenses.get("fixed_expenses", 0))
        nested.rows[1].cells[6].text = format_currency(expenses.get("net_potential", 0))
        nested.rows[2].cells[2].text = format_currency(expenses.get("variable_expenses", 0))
        nested.rows[2].cells[6].text = format_currency(expenses.get("total_est_expenses", 0))
        nested.rows[3].cells[2].text = format_currency(expenses.get("break_even", 0))
        nested.rows[3].cells[6].text = format_currency(expenses.get("amount_to_split", 0))
        nested.rows[4].cells[6].text = format_currency(expenses.get("walkout_potential", 0))


def update_fee_table(doc, shows, formatted_fee):
    for table in get_body_tables(doc):
        if "NET of any and all local withholding taxes." not in get_table_text(table):
            continue

        cell = table.rows[0].cells[0]
        if not cell.paragraphs:
            return

        set_paragraph_text(
            cell.paragraphs[0],
            f"Flat Guarantee of $ {formatted_fee} NET of any and all local withholding taxes.",
        )

        event_paragraphs = [p for p in cell.paragraphs[2:] if p.text.strip()]
        while len(event_paragraphs) < len(shows):
            event_paragraphs.append(cell.add_paragraph())

        for index, show in enumerate(shows):
            set_paragraph_text(
                event_paragraphs[index],
                f"Flat Guarantee of $ {formatted_fee} for the event on {show.get('date', '')}",
            )

        for extra in event_paragraphs[len(shows):]:
            set_paragraph_text(extra, "")
        return


def update_show_related_tables(doc, shows, formatted_fee):
    ticket_tables = find_body_tables(doc, is_ticket_pricing_table)
    ticket_summary_tables = find_body_tables(doc, is_ticket_summary_table)
    expense_tables = find_body_tables(doc, is_expense_table)

    for index, show in enumerate(shows):
        if index < len(ticket_tables):
            fill_ticket_pricing_table(ticket_tables[index], show)
        if index < len(ticket_summary_tables):
            fill_ticket_summary_table(ticket_summary_tables[index], show)
        if index < len(expense_tables):
            fill_expense_table(expense_tables[index], show)

    if len(shows) > 1:
        update_fee_table(doc, shows, formatted_fee)


def fill_single_show_details(doc, show):
    for table in get_body_tables(doc):
        text = get_table_text(table)
        if "DATE OF SHOW(S):" in text and "SCHEDULE" in text:
            table.rows[0].cells[0].text = f"DATE OF SHOW(S): {show['date']}"
            table.rows[1].cells[0].text = "NUMBER OF SHOW(S): 1"
            table.rows[2].cells[0].text = f"SHOW LENGTH: {show['show_length']}"
            table.rows[3].cells[0].text = f"ADDITIONAL ACTS: {show['additional_acts']}"
            table.rows[4].cells[0].text = f"CAPACITY: {show['capacity']}"
            table.rows[5].cells[0].text = f"SCHEDULE: {show['time']}"
        elif "VENUE:" in text and "Address:" in text:
            table.rows[0].cells[0].text = f"VENUE: {show['venue']}"
            table.rows[1].cells[0].text = f"Address: {show['venue_address']}"

def replace_nth_occurrence(doc, label, value, occurrence_index):
    count = 0

    for paragraph in doc.paragraphs:
        full_text = "".join(run.text for run in paragraph.runs)

        if label in full_text:
            if count == occurrence_index:
                before, _, _ = full_text.partition(label)
                new_text = before + f"{label} {value}"

                for run in paragraph.runs:
                    run.text = ""

                if paragraph.runs:
                    paragraph.runs[0].text = new_text
                return

            count += 1

    for table in get_all_tables(doc):
        for row in table.rows:
            for cell in row.cells:
                if label in cell.text:
                    if count == occurrence_index:
                        before, _, _ = cell.text.partition(label)
                        cell.text = before + f"{label} {value}"
                        return

                    count += 1


def replace_schedule_preserve_format(doc, value, occurrence_index):
    count = 0

    def normalize(text):
        return text.lower().replace(" ", "")

    # 🔴 Handle tables (your schedule is here)
    for table in get_all_tables(doc):
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    runs = paragraph.runs

                    if not runs:
                        continue

                    full_text = "".join(run.text for run in runs)
                    normalized_text = normalize(full_text)

                    if "cityschedule:" in normalized_text:
                        if count == occurrence_index:
                            # 🔥 Find where the label ends across runs
                            combined = ""
                            for i, run in enumerate(runs):
                                combined += run.text

                                if "schedule" in combined.lower():
                                    # Find colon in remaining runs
                                    for j in range(i, len(runs)):
                                        if ":" in runs[j].text:
                                            # 👉 Inject value HERE (preserves formatting)
                                            runs[j].text += f" {value}"
                                            return
                        count += 1

def fill_show_sections(doc, shows):
    show_tables = get_show_tables(doc)

    for index, show in enumerate(shows):
        if index >= len(show_tables):
            break

        fill_show_table(
            show_tables[index],
            show,
            show["show_length"],
            show["capacity"],
            show["additional_acts"],
        )


def fill_signature_table(doc, data):
    for table in get_body_tables(doc):
        if "Buyer Name" not in get_table_text(table):
            continue

        nested = table.rows[0].cells[0].tables[0]
        values = [
            "[sig|req|signer1]",
            data["buyer_name"],
            data["buyer_company_name"],
            format_header_date(data["signature_date"])
        ]
        replace_targets = ["[sig|req|signer1]", "Buyer Name", "Buyer Company name", "[date|date|signer1]"]

        for row in nested.rows:
            for cell in row.cells:
                for target, value in zip(replace_targets, values):
                    if target in cell.text:
                        cell.text = cell.text.replace(target, value)
        return


def build_performance_contract(data: PerformanceContractData) -> bytes:
    template_name = (
        "performance_single" if data.number_of_shows == 1 else "performance_multi"
    )
    doc = get_template(template_name)
    normalized = normalize_performance_contract(data)
    if data.number_of_shows > 2:
        ensure_repeated_tables(doc, data.number_of_shows)

    try:
        fee_value = float(data.fee)
    except (ValueError, TypeError):
        fee_value = 0.0

    formatted_fee = f"{fee_value:.2f}"
    replace_fee(doc, formatted_fee)
    update_template_headers(doc, normalized)

    replace_everywhere(doc, "PURCHASER NAME:", normalized["purchaser_name"])
    replace_nth_occurrence(doc, "Address:", normalized["purchaser_address"], 0)
    replace_everywhere(doc, "Signatory:", normalized["signatory"])
    replace_everywhere(doc, "COMPANY NAME:", normalized["company_name"])
    replace_nth_occurrence(doc, "Address:", normalized["company_address"], 1)
    replace_everywhere(doc, "VENUE:", normalized["venue"])
    replace_everywhere(doc, "DATE OF SHOW(S):", format_contract_date(normalized["date"]))
    replace_everywhere(
        doc,
        "Company is furnishing the services of ARTIST:",
        normalized["artist"],
    )

    replace_everywhere(doc, "NUMBER OF SHOW(S):", str(normalized["number_of_shows"]))
    replace_everywhere(doc, "SHOW LENGTH:", normalized["show_length"])
    replace_everywhere(doc, "ADDITIONAL ACTS:", normalized["additional_acts"])
    replace_everywhere(doc, "CAPACITY:", normalized["capacity"])

    replace_everywhere(doc, "Air Transportation:", normalized["air_transportation"])
    replace_everywhere(doc, "Hotel Accommodations:", normalized["hotel_accommodations"])
    replace_everywhere(doc, "Air Freight & Excess Baggage:", normalized["air_freight"])
    replace_everywhere(doc, "Ground Transportation:", normalized["ground_transportation"])
    replace_everywhere(doc, "Meals & Incidentals:", normalized["meals_incidentals"])

    replace_everywhere(doc, "SPECIAL PROVISIONS:", normalized["special_provisions"])
    replace_everywhere(doc, "Concessionaire fee:", normalized["concessionaire_fee"])
    replace_everywhere(doc, "Seller:", normalized["seller"])
    replace_everywhere(doc, "Hard Merchandising:", normalized["hard_merchandising"])
    replace_everywhere(doc, "Soft Merchandising:", normalized["soft_merchandising"])
    replace_everywhere(doc, "COMPLIMENTARY TICKETS:", normalized["complimentary_tickets"])

    replace_everywhere(
        doc,
        "Artist Name - 100% Headliner",
        f"{data.artist} - 100% Headliner",
    )

    fill_after_header(doc, "PRODUCTION & CATERING", normalized["production_catering"])
    fill_after_header(doc, "ADDITIONAL ADDENDA", normalized["additional_addenda"])
    fill_after_header(doc, "MERCHANDISING", normalized["merchandising_terms"])
    fill_signature_table(doc, normalized)

    raw_shows = normalized["shows"] or [
        {
            "date": normalized["date"],
            "venue": normalized["venue"],
            "venue_address": normalized["venue"],
            "time": "",
            "notes": normalized["additional_acts"],
            "capacity": normalized["capacity"],
            "show_length": normalized["show_length"],
            "city": normalized["city"],
        }
    ]
    normalized_shows = [normalize_show(show, normalized) for show in raw_shows]

    if data.number_of_shows > 1:
        fill_show_sections(doc, normalized_shows)
    else:
        fill_single_show_details(doc, normalized_shows[0])

    update_show_related_tables(doc, normalized_shows[: data.number_of_shows], formatted_fee)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return buffer.getvalue()


def build_nda_contract(data: NDAContractData, template: str):
    return template.format(
        disclosing_party=data.disclosing_party,
        receiving_party=data.receiving_party,
        purpose=data.purpose,
        duration=data.duration,
    )
