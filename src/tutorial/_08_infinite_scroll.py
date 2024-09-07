from fasthtml.common import Div, Table, Tbody, Td, Th, Thead, Tr, fast_app

app, rt = fast_app()


# fmt: off
@app.get
def page():
    return Div(
        Table(
            Thead(Tr(Th("Name"), Th("ID"))),
            Tbody(load_contacts(page=1)),
        ),
        cls="container",
    )
# fmt: on


@app.get
def load_contacts(page: int, limit: int = 5):
    rows = [Tr(Td("Smith"), Td((page - 1) * limit + i)) for i in range(1, limit)]
    return *rows, make_last_row(page, limit)


def make_last_row(page, limit):
    return Tr(
        Td("Smith"),
        Td(page * limit),
        hx_trigger="revealed",
        hx_swap="afterend",
        hx_get=load_contacts.rt(page=page + 1),
    )


DESC = "Demonstrates infinite scrolling of a page"
DOC = """
The infinite scroll pattern provides a way to load content dynamically on user scrolling action.

Let’s focus on the final row (or the last element of your content):
::make_last_row load_contacts::
This last element contains a listener which, when scrolled into view, will trigger a request. The result is then appended after it. The last element of the results will itself contain the listener to load the next page of results, and so on.

<blockquote><ins>revealed</ins> triggered when an element is scrolled into the viewport (also useful for lazy-loading). If you are using overflow in css like overflow-y: scroll you should use intersect once instead of revealed.</blockquote>
"""
