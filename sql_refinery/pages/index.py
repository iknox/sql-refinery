"""The home page of the app."""

from sql_refinery import styles
from sql_refinery.templates import template

import reflex as rx


@template(route="/", title="Home")
def index() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    with open("README.md", encoding="utf-8") as readme:
        content = readme.read()
    return rx.markdown(content, component_map=styles.markdown_style)
