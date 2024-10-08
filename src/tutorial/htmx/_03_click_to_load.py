from fasthtml.common import Button, Div, Table, Tbody, Td, Th, Thead, Tr, fast_app

app, rt = fast_app()


# fmt: off
@app.get
def page():
    return Div(cls="container overflow-auto")(
        Table(
            Thead(Tr(Th("Name"), Th("ID"))),
            Tbody(load_contacts(page=1)),
        )
    )



@app.get("/contacts")
def load_contacts(page: int, limit: int = 5):
    rows = [Tr(Td("Smith"), Td((page - 1) * limit + i)) for i in range(limit)]
    return *rows, make_last_row(page)


def make_last_row(page):
    return Tr(hx_target="this")(
        Td(colspan="3")(
            Button("Load More Agents...",
                   hx_get=load_contacts.rt(page=page + 1), hx_swap="outerHTML", cls="btn primary"),
        ),
    )
# fmt: on


DESC = "Demonstrates clicking to load more rows in a table"
DOC = """
This example shows how to implement click-to-load the next page in a table of data. The crux of the demo is the final row:
::make_last_row load_contacts::
This row contains a button that will replace the entire row with the next page of results (which will contain a button to load the next page of results). And so on.
"""
