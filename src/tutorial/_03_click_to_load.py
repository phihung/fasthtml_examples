from fasthtml.common import Button, Div, Table, Tbody, Td, Th, Thead, Tr, fast_app

app, rt = fast_app()


# fmt: off
@app.get("/table")
def contact_table():
    return Div(
        Table(
            Thead(Tr(Th("Name"), Th("ID"))),
            Tbody(load_contacts(page=1)),
        ),
        cls="container overflow-auto",
    )
# fmt: on


@app.get("/contacts")
def load_contacts(page: int, limit: int = 5):
    rows = [Tr(Td("Smith"), Td(page * limit + i)) for i in range(limit)]
    return *rows, make_last_row(page)


def make_last_row(page):
    return Tr(
        Td(
            Button(
                "Load More Agents...",
                hx_get=f"/contacts?page={page + 1}",
                hx_swap="outerHTML",
                cls="btn primary",
            ),
            colspan="3",
        ),
        hx_target="this",
    )


DESC = "Demonstrates clicking to load more rows in a table"
DOC = """
This example shows how to implement click-to-load the next page in a table of data. The crux of the demo is the final row:
::make_last_row load_contacts::
This row contains a button that will replace the entire row with the next page of results (which will contain a button to load the next page of results). And so on.
"""
