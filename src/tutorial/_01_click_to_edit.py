from collections import namedtuple

from fasthtml.common import Button, Div, Form, Input, Label, P, fast_app

app, rt = fast_app()

Contact = namedtuple("Contact", ["name", "email"])
current = Contact("Joe", "joe@blow.com")


@app.get("/contact/1")
def get_contact():
    return Div(
        Div(P(f"Name : {current.name}")),
        Div(P(f"Email : {current.email}")),
        Button("Click To Edit", hx_get="/contact/1/edit", cls="btn primary"),
        hx_target="this",
        hx_swap="outerHTML",
        cls="container",
    )


@app.get("/contact/1/edit")
def contact_edit():
    return Form(
        Div(Label("Name"), Input(type="text", name="name", value=current.name)),
        Div(Label("Email"), Input(type="email", name="email", value=current.email)),
        Button("Submit", cls="btn"),
        Button("Cancel", hx_get="/contact/1", cls="btn"),
        hx_put="/contact/1",
        hx_target="this",
        hx_swap="outerHTML",
        cls="container",
    )


@app.put("/contact/1")
def put_contact(c: Contact):
    global current
    current = c
    return get_contact()


DESC = "Demonstrates inline editing of a data object"
DOC = """
The click to edit pattern provides a way to offer inline editing of all or part of a record without a page refresh.

 - This pattern starts with a UI that shows the details of a contact. The div has a button that will get the editing UI for the contact from /contact/1/edit

::get_contact::
 
 - This returns a form that can be used to edit the contact

::contact_edit::

The form issues a PUT back to /contact/1, following the usual REST-ful pattern.

::put_contact::
"""
