import time
from pathlib import Path

from fasthtml.common import H3, Div, Img, Input, Span, Table, Tbody, Td, Th, Thead, Tr, fast_app

app, rt = fast_app()


# fmt: off
@app.get
def page():
    return Div(
        H3("Search Contacts"),
        Input(
            hx_post=search, hx_target="#results",
            hx_trigger="input changed delay:500ms, search", hx_indicator=".htmx-indicator",
            type="search", name="query", placeholder="Begin Typing To Search Users...",
        ),
        Span(Img(src="/img/bars.svg"), "Searching...", cls="htmx-indicator"),
        Table(
            Thead(Tr(Th("First Name"), Th("Last Name"), Th("Email"))),
            Tbody(id="results"),
        ),
    )
# fmt: on


@app.post
def search(query: str, limit: int = 10):
    time.sleep(0.5)
    data = [x.split(",") for x in LINES if query.lower() in x.lower()]
    return [Tr(Td(x[0]), Td(x[1]), Td(x[2])) for x in data[:limit]]


LINES = Path("public/data/contacts.csv").read_text().splitlines()


DESC = "Demonstrates the active search box pattern"
DOC = """
This example actively searches a contacts database as the user enters text.

We start with a search input and an empty table:
::page::
The input issues a POST to /search on the input event and sets the body of the table to be the resulting content. Note that the keyup event could be used as well, but would not fire if the user pasted text with their mouse (or any other non-keyboard method).

We add the delay:500ms modifier to the trigger to delay sending the query until the user stops typing. Additionally, we add the changed modifier to the trigger to ensure we don’t send new queries when the user doesn’t change the value of the input (e.g. they hit an arrow key, or pasted the same value).

Since we use a search type input we will get an x in the input field to clear the input. To make this trigger a new POST we have to specify another trigger. We specify another trigger by using a comma to separate them. The search trigger will be run when the field is cleared but it also makes it possible to override the 500 ms input event delay by just pressing enter.

Finally, we show an indicator when the search is in flight with the hx-indicator attribute.
"""
