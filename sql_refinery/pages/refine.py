"""The refine page."""

from sql_refinery.templates import template
from sqlglot.optimizer import optimize

import reflex as rx

class ReactDiffViewerContinued(rx.Component):
    """React component for react-diff-viewer-continued.
    https://github.com/Aeolun/react-diff-viewer-continued
    """

    # The name of the npm package.
    library = "react-diff-viewer-continued"

    # The name of the component to use from the package.
    tag = "ReactDiffViewer"

    # Spline is a default export from the module.
    is_default = False

    # Any props that the component takes.
    oldValue: rx.Var[str]
    newValue: rx.Var[str]
    splitView: rx.Var[bool]

diff_viewer = ReactDiffViewerContinued.create

class Spline(rx.Component):
    """Spline component."""

    # The name of the npm package.
    library = "@splinetool/react-spline"

    # Any additional libraries needed to use the component.
    lib_dependencies: list[str] = [
        "@splinetool/runtime@1.5.5"
    ]

    # The name of the component to use from the package.
    tag = "Spline"

    # Spline is a default export from the module.
    is_default = True

    # Any props that the component takes.
    scene: rx.Var[str]


# Convenience function to create the Spline component.
spline = Spline.create



class State(rx.State):
    """The app state."""

    dialect: str = ""
    optimized_query: str = ""
    raw_query: str = ""

    def refine(self, form_data: dict[str, str]):
        """Refine a sql query"""
        self.raw_query = form_data.get("raw_query")
        self.dialect = form_data.get("dialect")
        self.optimized_query = optimize(self.raw_query, dialect=self.dialect).sql()

    # TODO: There is almost certainly a better way to handle this state. 
    # I need to read up on reflex core concepts I think.
    
    def reset_optimized_sql(self):
        """Resets optimized sql state"""
        self.optimized_query = ""

    def reset_all(self):
        """Resets all state"""
        self.dialect = ""
        self.optimized_query = ""
        self.raw_query = ""

input_view = rx.box(
    rx.heading("Refine SQL", size="8"),
    rx.form(
        rx.text_area(
            name="raw_query",
            placeholder="SELECT x ...",
            auto_focus=True,
            required=True,
            width="100%",
            rows="25",
            resize="both",
            value=State.raw_query,
            on_change=State.set_raw_query,
        ),
        rx.hstack(
            rx.select.root(
                rx.select.trigger(),
                rx.select.content(
                    rx.select.group(
                        rx.select.label("Select Database Dialect"),
                        rx.select.item("Databricks", value="databricks"),
                        rx.select.item("Presto", value="presto"),
                        rx.select.item("Redshift", value="redshift"),
                        rx.select.item("Snowflake", value="snowflake"),
                    )
                ),
                default_value=rx.cond(State.dialect,  State.dialect, "snowflake"),
                name="dialect",
            ),
            rx.button("Refine SQL"),
        ),
        on_submit=State.refine,
    ),
    rx.button("Reset form", on_click=State.reset_all),
    width="100%",
)

optimized_view = rx.box(
    rx.heading("Refined SQL", size="8"),
    rx.text(State.raw_query),
    rx.text(State.optimized_query),
    diff_viewer(oldvalue="b", newvalue="f", splitview=True),
    #spline(
    #    scene="https://prod.spline.design/joLpOOYbGL-10EJ4/scene.splinecode"
    #),
    rx.button("Try again", on_click=State.reset_optimized_sql),
    width="100%",
)


@template(route="/refine", title="Refine")
def refine() -> rx.Component:
    """The refine page.

    Returns:
        The UI for the refine page.
    """
    return rx.flex(
        rx.vstack(
            rx.cond(
                ~State.optimized_query,
                input_view,
                optimized_view,
            ),
            width="100%",
        ),
        width="100%",
    )
