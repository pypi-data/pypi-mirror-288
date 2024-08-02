"""This module contains the ui and the server for creating a new invoice."""

import datetime
import io
from pathlib import Path
from string import Template

import pandas as pd
from shiny import module, ui, render, reactive
from tinydb import TinyDB, Query


@module.ui
def new_invoice_ui(config):
    """Defines the shiny ui for new invoices"""
    invoice_defaults = config.invoice_defaults

    return ui.layout_column_wrap(
        ui.card(
            ui.card_header("Invoice Details"),
            ui.output_ui(id="invoice_number_ui", width="100%"),
            ui.input_date(id="created_at_date", label="Created At", width="100%"),
            ui.output_ui(id="due_date_ui", width="100%"),
            ui.input_text(
                id="introduction",
                label="Introduction",
                value=invoice_defaults.introduction,
                width="100%",
            ),
            ui.input_text_area(
                id="recipient_address",
                label="Recipient Address",
                value=invoice_defaults.recipient,
                rows=3,
                width="100%",
            ),
            ui.tooltip(
                ui.input_text_area(
                    id="invoice_items",
                    label="Invoice Items",
                    value=invoice_defaults.items,
                    rows=6,
                    width="100%",
                    spellcheck=True,
                ),
                "Should be in csv format. The last column will be used to calculate the"
                "total price. The values should be before taxes.",
            ),
            ui.download_button(id="download_button", label="Download Invoice", width="100%"),
        ),
        ui.card(
            ui.card_header("Rendered Invoice"), ui.output_ui(id="rendered_invoice_ui", width="100%")
        ),
    )


@module.server
def new_invoice_server(input, _, __, config):
    """Contains the Shiny Server for creating new invoices"""
    datastore = TinyDB(config.paths.datastore)

    with open(Path(config.paths.html_template), "r", encoding="utf8") as file:
        html_template = Template(file.read())

    @reactive.calc
    def parse_invoice_items() -> pd.DataFrame:
        return pd.read_csv(io.StringIO(input.invoice_items()), sep=",")

    @reactive.calc
    def convert_invoice_csv_to_html() -> str:
        return parse_invoice_items().to_html(index=False, border=0)

    @reactive.calc
    def calculate_totals():
        items = parse_invoice_items()
        last_column = items.columns[-1]
        items[last_column] = (
            items[last_column].str.replace(".", "").str.replace("€", "").astype(float)
        )
        return items[last_column].sum()

    @render.ui
    def invoice_number_ui():
        invoice_ids = [int(invoice.get("Id")) for invoice in datastore.all()]
        next_id = 1
        if invoice_ids:
            next_id = max(invoice_ids) + 1
        number_ui = ui.input_text(
            id="invoice_number", label="Invoice Number", value=str(next_id), width="100%"
        )
        return number_ui

    @render.ui
    def due_date_ui():
        payment_terms_days = config.company.payment_terms_days
        due_date = input.created_at_date() + datetime.timedelta(days=payment_terms_days)
        return ui.input_date("due_date", "Due date", value=str(due_date), width="100%")

    @reactive.calc
    def customer_name():
        return input.recipient_address().split("\n")[0]

    @reactive.effect
    @reactive.event(input.invoice_number)
    def already_existing_id_modal():
        query = Query()
        already_existing = datastore.search(query.Id == input.invoice_number())
        if already_existing:
            ui.notification_show(
                "This invoice already exists. Please choose another invoice number.",
                type="error",
                duration=2,
            )

    @render.download(
        filename=lambda: f"{input.invoice_number()}.html",
    )
    def download_button():
        """Download the currently created invoice"""
        datastore.insert(
            {
                "Id": input.invoice_number(),
                "Created At": str(input.created_at_date()),
                "Due Date": str(input.due_date()),
                "Paid At": "Unpaid",
                "Customer": customer_name(),
            }
        )
        ui.notification_show(
            "Reload page to update 'Existing Invoices' view.", type="message", duration=None
        )
        with io.BytesIO() as buf:
            buf.write(render_invoice().encode("utf8"))
            yield buf.getvalue()

    @reactive.calc
    def render_invoice():
        total_net = calculate_totals()
        company = config.company
        tax = total_net * float(company.tax_rate)
        total_gross = total_net + tax
        substitutions = {
            "name": company.name,
            "primary_skills": " | ".join(company.skills[:2]),
            "all_skills": "<br/>".join(company.skills),
            "piped_address": " | ".join(company.address),
            "linebreaked_address": "<br/>".join(company.address),
            "primary_contact": "<br/>".join(company.contact[:2]),
            "bank": company.bank.name,
            "iban": company.bank.iban,
            "bic": company.bank.bic,
            "tax_number": company.bank.tax_number,
            "tax_rate": f"{float(company.tax_rate) * 100}%",
            "all_contact": "<br/>".join(company.contact),
            "invoice_number": input.invoice_number(),
            "created_at_date": input.created_at_date().strftime("%d.%m.%Y"),
            "due_at_date": input.due_date().strftime("%d.%m.%Y"),
            "introduction": input.introduction(),
            "recipient_address": "</br>".join(input.recipient_address().split("\n")),
            "invoice_items": convert_invoice_csv_to_html(),
            "total_net": f"{total_net:n} €",
            "tax": f"{tax:n} €",
            "total_gross": f"{total_gross:n} €",
        }
        return html_template.substitute(substitutions)

    @render.ui
    def rendered_invoice_ui():
        """Render the currently configured invoice"""
        return ui.HTML(render_invoice())
