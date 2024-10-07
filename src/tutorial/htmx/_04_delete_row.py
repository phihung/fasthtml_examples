from fasthtml.common import Button, Div, Style, Table, Tbody, Td, Th, Thead, Tr, fast_app

css = """\
tr.htmx-swapping td {
  opacity: 0;
  transition: opacity 1s ease-out !important;
}
"""

app, rt = fast_app(hdrs=[Style(css)])


@app.get
def page():
    return Div(cls="container overflow-auto")(
        Table(
            Thead(Tr(Th("Name"), Th("Email"), Th())),
            Tbody(hx_confirm="Are you sure?", hx_target="closest tr", hx_swap="outerHTML swap:1s")(
                Tr(
                    Td("Joe Smith"),
                    Td("joe@smith.org"),
                    Td(Button("Delete", hx_delete="/contacts/0", cls="btn secondary")),
                ),
                Tr(
                    Td("Angie MacDowell"),
                    Td("angie@macdowell.org"),
                    Td(Button("Delete", hx_delete="/contacts/1", cls="btn secondary")),
                ),
                Tr(
                    Td("Fuqua Tarkenton"),
                    Td("fuqua@tarkenton.org"),
                    Td(Button("Delete", hx_delete="/contacts/2", cls="btn secondary")),
                ),
                Tr(
                    Td("Kim Yee"),
                    Td("kim@yee.org"),
                    Td(Button("Delete", hx_delete="/contacts/3", cls="btn secondary")),
                ),
            ),
        ),
    )


@rt("/contacts/{idx}")
def delete(idx: int):
    # Delete actual data here
    return None


DESC = "Demonstrates row deletion in a table"
DOC = """
This example shows how to implement a delete button that removes a table row upon completion. First let’s look at the table body:
```python
Table(
    Thead(),
    Tbody(
        Tr(), Tr(), Tr(), Tr(),
        hx_confirm="Are you sure?",
        hx_target="closest tr",
        hx_swap="outerHTML swap:1s",
    )
)
```
The table body has a `hx-confirm` attribute to confirm the delete action. It also set the target to be the closest tr that is, the closest table row, for all the buttons (hx-target is inherited from parents in the DOM.) The swap specification in hx-swap says to swap the entire target out and to wait 1 second after receiving a response. This last bit is so that we can use the following CSS:
::css::
To fade the row out before it is swapped/removed.

Each row has a button with a hx-delete attribute containing the url on which to issue a DELETE request to delete the row from the server. This request responds with a 200 status code and empty content, indicating that the row should be replaced with nothing.
```python
Tr(
    Td("Angie MacDowell"),
    Td("angie@macdowell.org"),
    Td(Button("Delete", hx_delete="/contacts/1", cls="btn secondary")),
)
```
"""
HEIGHT = "350px"
