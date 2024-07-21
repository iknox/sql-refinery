"""The settings page."""

from sql_refinery.templates import ThemeState, template

import reflex as rx


@template(route="/settings", title="Settings")
def settings() -> rx.Component:
    """The settings page.

    Returns:
        The UI for the settings page.
    """
    return rx.vstack(
        rx.heading("Settings", size="8"),
        rx.hstack(
            rx.text("Dark mode: "),
            rx.color_mode.switch(),
        ),
    )
