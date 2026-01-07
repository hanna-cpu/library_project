import reflex as rx


def navigation_bar(state_class) -> rx.Component:
    """Common navigation bar component used across all pages."""
    return rx.hstack(
        rx.heading(
            f"User: ",
            rx.text(state_class.username, as_="span", font_weight="bold"),
            size="6",
        ),
        rx.spacer(),
        rx.button(
            "Login Page",
            on_click=state_class.navigate_to_loginpage,
            size="3",
            variant="solid",
            color_scheme="blue",
        ),

        rx.spacer(),
        rx.button(
            "Home Page",
            on_click=state_class.navigate_to_homepage,
            size="3",
            variant="solid",
            color_scheme="blue",
        ),
        rx.spacer(),
        rx.button(
            "Borrow Books",
            on_click=state_class.navigate_to_borrow,
            size="3",
            variant="solid",
            color_scheme="blue",
        ),
        rx.button(
            "Return Books",
            on_click=state_class.navigate_to_return,
            size="3",
            variant="solid",
            color_scheme="jade",
        ),
        rx.container(
            rx.color_mode.button(position="top-right"),
        ),
        width="100%",
        padding="1rem",
        background_color="lightblue",
        align="center",
    )


def page_container(state_class, *children) -> rx.Component:
    """Common page container with navigation bar."""
    return rx.box(
        navigation_bar(state_class),
        *children,
        width="100%",
        min_height="100vh",
        on_mount=state_class.set_username_from_query,
    )