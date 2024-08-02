"""This module contains the ui and server configurations for the existing invoices."""

import datetime
from pathlib import Path

import pandas as pd
from shiny import module, ui, render, reactive
from tinydb import TinyDB, Query  # pylint: disable=import-error
from tinydb.operations import set as db_set  # pylint: disable=import-error


@module.ui
def existing_invoices_ui():
    """Defines the shiny ui for existing invoices"""
    return ui.div(
        ui.card(
            ui.card_header("Filter"),
            ui.layout_columns(
                ui.tooltip(
                    ui.input_text("invoice_numbers", "Filter by invoices", placeholder="13,21,37"),
                    "Comma separated",
                ),
                ui.input_date_range(
                    id="daterange",
                    label="Filter by Date range",
                    start=f"{datetime.date.today().year}-01-01",
                ),
                ui.input_checkbox_group(
                    id="paid_status",
                    label="Paid Status",
                    choices={"paid": "Paid", "unpaid": "Unpaid"},
                    inline=True,
                ),
            ),
        ),
        ui.card(
            ui.layout_column_wrap(
                ui.card(
                    ui.card_header("List of filtered invoices"),
                    ui.output_data_frame("invoice_list"),
                ),
                ui.card(ui.card_header("Selected Invoice"), ui.output_ui("selected_invoice")),
            )
        ),
    )


@module.server
def existing_invoices_server(input, _, __, config):
    """Contains the Shiny Server for existing invoices"""

    datastore = TinyDB(config.paths.datastore)

    @reactive.calc
    def get_filtered_invoices() -> pd.DataFrame | str:
        """Retrieve all invoices from the datastore and turn them into a DataFrame.
        The input filters will then be applied to the dataframe such that only the desired results
        will be returned.
        """
        selected_invoices = datastore.all()
        for invoice in selected_invoices:
            invoice["Link"] = ui.a("Download", href=f"{invoice["Id"]}.html", target="_blank")
        df = pd.DataFrame.from_records(selected_invoices)
        if len(df) == 0:
            return df
        df = _filter_invoices(df)
        df["Created At"] = df["Created At"].apply(lambda x: x.strftime("%d.%m.%Y"))
        df["Due Date"] = df["Due Date"].apply(lambda x: x.strftime("%d.%m.%Y"))
        df["Paid At"] = df["Paid At"].apply(
            lambda x: (
                datetime.datetime.strptime(x, "%Y-%m-%d").strftime("%d.%m.%Y")
                if x != "Unpaid"
                else "Unpaid"
            )
        )
        return df

    def _filter_invoices(df):
        if input.invoice_numbers():
            filtered_ids = input.invoice_numbers().split(",")
            df = df.loc[df["Id"].isin(filtered_ids)]
        if input.paid_status():
            paid, unpaid = pd.DataFrame(), pd.DataFrame()
            if "paid" in input.paid_status():
                paid = df.loc[df["Paid At"] != "Unpaid"]
            if "unpaid" in input.paid_status():
                unpaid = df.loc[df["Paid At"] == "Unpaid"]
            df = pd.concat([paid, unpaid])
        df["Created At"] = pd.to_datetime(df["Created At"]).dt.date
        df["Due Date"] = pd.to_datetime(df["Due Date"]).dt.date
        start_date = input.daterange()[0]
        end_date = input.daterange()[1]
        df = df[(df["Created At"] >= start_date) & (df["Created At"] <= end_date)]
        return df

    @render.data_frame
    def invoice_list():
        """Render a list of filtered invoices"""
        df = get_filtered_invoices()
        table = render.DataGrid(df, selection_mode="rows", width="100%", editable=True)
        return table

    def patch_table(patch):
        """Apply edits to the table only if the fourth column 'Paid At' was changed"""
        table_data = invoice_list.data()
        if patch.get("column_index") != 3:
            column_index = patch.get("column_index")
            edited_column = table_data.columns[int(column_index)]
            ui.notification_show(
                "You can only edit the column 'Paid At'.",
                type="warning",
                duration=2,
            )
            return table_data[edited_column].iloc[patch.get("row_index")]
        try:
            query = Query()
            invoice_id = table_data.iloc[patch.get("row_index")]["Id"]
            parsed_date = datetime.datetime.strptime(patch.get("value"), "%d.%m.%Y")
            datastore.update(
                db_set("Paid At", parsed_date.strftime("%Y-%m-%d")), query.Id == invoice_id
            )
        except Exception:  # pylint: disable=broad-exception-caught
            ui.notification_show(
                "Error while updating invoice, please only use the date format '%d.%m.%Y'.",
                type="error",
                duration=6,
            )
        return patch.get("value")

    invoice_list.set_patch_fn(patch_table)

    @render.ui
    def selected_invoice():
        """Render the currently selected invoice"""
        selection = invoice_list.cell_selection()["rows"]
        if len(selection) > 0:
            selection = selection[0]
            df = get_filtered_invoices().iloc[selection]["Link"]
            root_dir = Path(config.paths.invoices_dir)
            with open(root_dir / df.attrs.get("href"), "r", encoding="utf8") as file:
                html = file.read()
            return ui.HTML(html)
        return selection
