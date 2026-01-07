import reflex as rx
from library_project.backend.borrow_backend import borrowState
from library_project.frontend.frontend_common import page_container


def borrow_page() -> rx.Component:
    """Borrow component with navigation bar and book selection table."""
    return page_container(
        borrowState,
        # Welcome message
        rx.center(
            rx.vstack(
                rx.heading(
                    f"Borrow Books - ",
                    rx.text(borrowState.username, as_="span", color="blue"),
                    size="7",
                ),
                rx.text(
                    "Select books to borrow from the list below.",
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
                        rx.table.column_header_cell("Availability"),
                        rx.table.column_header_cell("Add to Borrow List"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        borrowState.books_data,
                        lambda book: rx.table.row(
                            rx.table.cell(book["title"]),
                            rx.table.cell(book["author"]),
                            rx.table.cell(
                                rx.badge(
                                    book["availability"],
                                    color_scheme=rx.cond(
                                        book["availability"] == "Available",
                                        "green",
                                        "red"
                                    )
                                )
                            ),
                            rx.table.cell(
                                rx.checkbox(
                                    checked=borrowState.selected_books.contains(book["id"]),
                                    on_change=lambda: borrowState.toggle_book_selection(book["id"]),
                                    disabled=book["availability"] == "Unavailable",
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
                "Confirm Borrows",
                on_click=borrowState.confirm_borrows,
                size="3",
                variant="solid",
                color_scheme="blue",
                disabled=borrowState.selected_books.length() == 0,
            ),
            padding="1.5rem",
        ),
    )