"""The refine page."""

from sql_refinery.templates import template
from sqlglot.optimizer import optimize

import reflex as rx


class State(rx.State):
    """The app state."""

    raw_query = ""
    optimized_query = ""
    dialect = ""

    def refine(self):
        """Refine a sql query"""
        self.optimized_query = optimize(self.raw_query, dialect=self.dialect)


@template(route="/refine", title="Refine")
def refine() -> rx.Component:
    """The refine page.

    Returns:
        The UI for the refine page.
    """
    return rx.flex(
        rx.vstack(
            rx.heading("Refine SQL", size="8"),
            rx.text_area(
                placeholder="SELECT x ...",
                auto_focus=True,
                required=True,
                width="100%",
                rows="25",
                resize="both",
            ),
            rx.hstack(
                rx.select(
                    ["Databricks", "Presto", "Redshift", "Snowflake"],
                    label="Select Database Dialect",
                    default_value="Snowflake",
                ),
                rx.button("Refine SQL"),
            ),
            width="100%",
        ),
        width="100%",
    )


app = rx.App()
