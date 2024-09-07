from fasthtml.common import Button, Div, Form, Input, Style, Table, Tbody, Td, Th, Thead, Tr, fast_app

css = """\
#toast.htmx-settling {
  opacity: 100;
}

#toast {
  opacity: 0;
  transition: opacity 3s ease-out !important;
  background: blue;
  color: orange;
}
"""

app, rt = fast_app(hdrs=[Style(css)])


@app.get
def page():
    # Bug with default enctype: multipart/form-data
    return Form(enctype="", hx_post=update.rt(), hx_swap="outerHTML settle:3s", hx_target="#toast", cls="container")(
        Table(
            Thead(Tr(Th("Name"), Th("Email"), Th("Active"))),
            Tbody(
                Tr(Td("Kim 1"), Td("kim@1.org"), Td(Input(type="checkbox", name="active:kim@1.org"))),
                Tr(Td("Kim 2"), Td("kim@2.org"), Td(Input(type="checkbox", name="active:kim@2.org"))),
                Tr(Td("Kim 3"), Td("kim@3.org"), Td(Input(type="checkbox", name="active:kim@3.org"))),
                Tr(Td("Kim 4"), Td("kim@4.org"), Td(Input(type="checkbox", name="active:kim@4.org"))),
            ),
        ),
        Button("Bulk Update", cls="btn primary"),
        Div(id="toast"),
    )


@app.post("/users")
def update(x: dict):
    n = len(x)
    return Div(f"Activated {n} and deactivated {4-n} users", id="toast", aria_live="polite")


DESC = "Demonstrates bulk updating of multiple rows of data"
DOC = """
This demo shows how to implement a common pattern where rows are selected and then bulk updated. This is accomplished by putting a form around a table, with checkboxes in the table, and then including the checked values in the form submission (POST request):

The server will bulk-update the statuses based on the values of the checkboxes. We respond with a small toast message about the update to inform the user, and use ARIA to politely announce the update for accessibility.
::css::
The cool thing is that, because HTML form inputs already manage their own state, we don’t need to re-render any part of the users table. The active users are already checked and the inactive ones unchecked!

You can see a working example of this code below.
::page update::
"""
