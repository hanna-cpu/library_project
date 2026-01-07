"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx


# Below we import all our frontend and baxkend files. 
# it is mandatory
from library_project.frontend.homepage import homepage_page 
from library_project.frontend.borrow_page import borrow_page
from library_project.frontend.return_page import return_page


from rxconfig import config


class State(rx.State):
    """The app state."""


## This is our Landing Page. It is the default page that the program shows
# it shows a Login as 2 different users.


def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Library Project", size="6"),
            rx.link("Login As User 1", href="homepage?username=lala"),
            rx.link("Login As User 2", href="homepage?username=lol"),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )

app = rx.App()
app.add_page(index)
app.add_page(homepage_page, route="/homepage")
app.add_page(borrow_page, route="/borrow")
app.add_page(return_page, route="/return")

