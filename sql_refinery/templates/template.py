"""Common templates used between pages in the app."""

from __future__ import annotations

from sql_refinery import styles
from sql_refinery.components.sidebar import sidebar
from typing import Callable

import reflex as rx

# Meta tags for the app.
default_meta = [
    {
        "name": "viewport",
        "content": "width=device-width, shrink-to-fit=no, initial-scale=1",
    },
]


class ThemeState(rx.State):
    """The state for the theme of the app."""

    accent_color: str = "ruby"
    gray_color: str = "gray"


def template(
    route: str | None = None,
    title: str | None = None,
    description: str | None = None,
    meta: str | None = None,
    script_tags: list[rx.Component] | None = None,
    on_load: rx.event.EventHandler | list[rx.event.EventHandler] | None = None,
) -> Callable[[Callable[[], rx.Component]], rx.Component]:
    """The template for each page of the app.

    Args:
        route: The route to reach the page.
        title: The title of the page.
        description: The description of the page.
        meta: Additionnal meta to add to the page.
        on_load: The event handler(s) called when the page load.
        script_tags: Scripts to attach to the page.

    Returns:
        The template with the page content.
    """

    def decorator(page_content: Callable[[], rx.Component]) -> rx.Component:
        """The template for each page of the app.

        Args:
            page_content: The content of the page.

        Returns:
            The template with the page content.
        """
        # Get the meta tags for the page.
        all_meta = [*default_meta, *(meta or [])]

        def templated_page():
            return rx.hstack(
                sidebar(),
                rx.box(
                    rx.vstack(
                        page_content(),
                        rx.spacer(),
                        **styles.template_content_style,
                    ),
                    **styles.template_page_style,
                ),
                align="start",
                background=f"radial-gradient(circle at top right, {rx.color('accent', 1)}, {rx.color('black', 4)});",
                position="relative",
            )

        @rx.page(
            route=route,
            title=title,
            description=description,
            meta=all_meta,
            script_tags=script_tags,
            on_load=on_load,
        )
        def theme_wrap():
            return rx.theme(
                templated_page(),
                has_background=True,
                accent_color=ThemeState.accent_color,
                gray_color=ThemeState.gray_color,
            )

        return theme_wrap

    return decorator
