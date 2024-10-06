from collections import namedtuple

from fasthtml.common import Button, Div, Form, Input, Label, P, fast_app

app, rt = fast_app()

Contact = namedtuple("Contact", ["name", "email"])
current = Contact("Joe", "joe@blow.com")


@app.get
def page():
    return get_contact()


@app.get("/contact")
def get_contact():
    return Div(hx_target="this", hx_swap="outerHTML", cls="container")(
        Div(P(f"Name : {current.name}")),
        Div(P(f"Email : {current.email}")),
        Button("Click To Edit", hx_get=contact_edit.rt(), cls="btn primary"),
    )


@app.get("/contact/edit")
def contact_edit():
    return Form(hx_put=put_contact.rt(), hx_target="this", hx_swap="outerHTML", cls="container")(
        Div(Label("Name"), Input(type="text", name="name", value=current.name)),
        Div(Label("Email"), Input(type="email", name="email", value=current.email)),
        Div(Button("Submit"), Button("Cancel", hx_get=get_contact.rt()), cls="grid"),
    )


@app.put("/contact")
def put_contact(c: Contact):
    global current
    current = c
    return get_contact()


DESC = "Demonstrates inline editing of a data object"
DOC = """
The click to edit pattern provides a way to offer inline editing of all or part of a record without a page refresh.

 - This pattern starts with a UI that shows the details of a contact. The div has a button that will get the editing UI for the contact from /contact/edit

::get_contact::
 
 - This returns a form that can be used to edit the contact

::contact_edit::

The form issues a PUT back to /contact, following the usual REST-ful pattern.

::put_contact::
"""
