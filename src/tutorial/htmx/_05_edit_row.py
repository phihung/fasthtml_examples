from fasthtml.common import Button, Div, Input, Table, Tbody, Td, Th, Thead, Tr, fast_app

app, rt = fast_app()

DATA = [
    ("Joe 1", "joe1@a.b"),
    ("Joe 2", "joe2@a.b"),
    ("Joe 3", "joe3@a.b"),
    ("Joe 4", "joe4@a.b"),
]


@app.get
def page():
    return Div(cls="container-fluid")(
        Table(
            Thead(Tr(Th("Name"), Th("Email"), Th())),
            Tbody(hx_target="closest tr", hx_swap="outerHTML")(
                tuple(get_contact(i) for i in range(4)),
            ),
        ),
    )


@app.get("/contact/{idx}")
def get_contact(idx: int):
    name, email = DATA[idx]
    return Tr(
        Td(name),
        Td(email),
        Td(Button("Edit", hx_get=f"/contact/{idx}/edit", hx_trigger="edit", onclick=JS)),
    )


@app.get("/contact/{idx}/edit")
def edit_view(idx: int):
    name, email = DATA[idx]
    return Tr(hx_trigger="cancel", hx_get=f"/contact/{idx}", cls="editing")(
        Td(Input(name="name", value=name)),
        Td(Input(name="email", value=email)),
        Td(cls="grid")(
            Button("Cancel", hx_get=f"/contact/{idx}", cls="btn secondary"),
            Button("Save", hx_put=f"/contact/{idx}", hx_include="closest tr", cls="btn primary"),
        ),
    )


@app.put("/contact/{idx}")
def put_contact(idx: int, x: dict):
    DATA[idx] = (x["name"], x["email"])
    return get_contact(idx)


JS = """
let editing = document.querySelector('.editing')
if(editing) {
    htmx.trigger(editing, 'cancel');
}
htmx.trigger(this, 'edit')
"""

# JS = """
# let editing = document.querySelector('.editing')
# if(editing) {
#     Swal.fire({
#         title: 'Already Editing',
#         showCancelButton: true,
#         confirmButtonText: 'Yep, Edit This Row!',
#         text:'Hey!  You are already editing a row!  Do you want to cancel that edit and continue?'
#     })
#     .then((result) => {
#         if(result.isConfirmed) {
#             htmx.trigger(editing, 'cancel')
#             htmx.trigger(this, 'edit')
#         }
#     })
# } else {
#     htmx.trigger(this, 'edit')
# }
# """

DESC = "Demonstrates how to edit rows in a table"
DOC = """
This example shows how to implement editable rows. First let’s look at the table body:
::page::
This will tell the requests from within the table to target the closest enclosing row that the request is triggered on and to replace the entire row.

Here is the HTML for a row:
::get_contact::
Javascript code
::JS::
Here we are getting a bit fancy and only allowing one row at a time to be edited, using some JavaScript. We check to see if there is a row with the .editing class on it and confirm that the user wants to edit this row and dismiss the other one. If so, we send a cancel event to the other row so it will issue a request to go back to its initial state.

We then trigger the edit event on the current element, which triggers the htmx request to get the editable version of the row.

Note that if you didn’t care if a user was editing multiple rows, you could omit the hyperscript and custom hx-trigger, and just let the normal click handling work with htmx. You could also implement mutual exclusivity by simply targeting the entire table when the Edit button was clicked. Here we wanted to show how to integrate htmx and JavaScript to solve the problem and narrow down the server interactions a bit, plus we get to use a nice SweetAlert confirm dialog.

Finally, here is what the row looks like when the data is being edited:
::edit_view::
Here we have a few things going on: First off the row itself can respond to the cancel event, which will bring back the read-only version of the row. There is a cancel button that allows cancelling the current edit. Finally, there is a save button that issues a PUT to update the contact. Note that there is an hx-include that includes all the inputs in the closest row. Tables rows are notoriously difficult to use with forms due to HTML constraints (you can’t put a form directly inside a tr) so this makes things a bit nicer to deal with.
"""
