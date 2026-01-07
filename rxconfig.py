import reflex as rx

config = rx.Config(
    app_name="library_project",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)