import reflex as rx
from library_project.backend.return_backend import returnState
from library_project.frontend.frontend_common import page_container


def return_page() -> rx.Component:
    """Return component with navigation bar and book selection table."""
    return page_container(
        returnState,
        # Welcome message
        rx.center(
            rx.vstack(
                rx.heading(
                    f"Return Books - ",
                    rx.text(returnState.username, as_="span", color="blue"),
                    size="7",
                ),
                rx.text(
                    "Select books to return from the list of your borrowed books below.",
                    size="4",
                    color="gray",
                ),
                spacing="2",
                padding_top="1.5rem",
            )
        ),
        
        # Books table
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Title"),
                        rx.table.column_header_cell("Author"),
                        rx.table.column_header_cell("Add to return List"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        returnState.books_data,
                        lambda book: rx.table.row(
                            rx.table.cell(book["title"]),
                            rx.table.cell(book["author"]),
                            rx.table.cell(
                                rx.checkbox(
                                    checked=returnState.selected_books.contains(book["id"]),
                                    on_change=lambda checked, book_id=book["id"]: returnState.toggle_book_selection(book_id),
                                )
                            ),
                        )
                    )
                ),
                variant="surface",
                width="100%",
            ),
            padding="2rem",
            width="90%",
            margin="0 auto",
        ),
        
        # Confirm button
        rx.center(
            rx.button(
                "Confirm returns",
                on_click=returnState.confirm_returns,
                size="3",
                variant="solid",
                color_scheme="blue",
                disabled=returnState.selected_books.length() == 0,
            ),
            padding="1.5rem",
        ),
    )