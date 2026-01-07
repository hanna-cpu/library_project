import reflex as rx
from library_project.backend.homepage_backend import HomepageState
from library_project.frontend.frontend_common import page_container


def homepage_page() -> rx.Component:
    """Homepage component with navigation bar and welcome message."""
    return page_container(
        HomepageState,
        # Welcome message
        rx.center(
            rx.vstack(
                rx.heading(
                    f"Welcome to the Library,  ",
                    rx.text(HomepageState.username, as_="span", color="blue"),
                    "!",
                    size="8",
                ),
                rx.text(
                    "Use the buttons above to borrow or return books.",
                    size="4",
                    color="gray",
                ),
                spacing="4",
                padding_top="4rem",
            )
        ),
    )