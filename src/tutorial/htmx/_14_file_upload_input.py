from fasthtml.common import Button, Div, Form, Input, Label, fast_app
from starlette.datastructures import UploadFile

app, rt = fast_app()

form_name = "binaryForm"


def my_form(*children):
    return Form(enctype="multipart/form-data", hx_swap="outerHTML", hx_post=submit, hx_target="this", id=form_name)(
        Button("Submit"),
        *children,
    )


@app.get
def page():
    return Div(
        # Move file input out of the form
        Label("An error should happen when you click on submit button. But the uploaded file should NOT be cleared"),
        Input(form=form_name, type="file", name="binaryFile"),
        my_form(),
    )


@app.post
async def submit(binaryFile: UploadFile):
    return my_form(Div("Error: Try again", style="color:red"))


@rt
def bad_form():
    # This bad implementation
    # Users are required to re-upload the file in case of error on other fields
    return Form(hx_swap="outerHTML", hx_post=bad_form, hx_target="this")(
        Input(type="file", name="binaryFile"),
        Button("Submit"),
    )


DESC = "Demonstrates how to preserve file inputs after form errors"
DOC = """
When using server-side error handling and validation with forms that include both primitive values and file inputs, the file input’s value is lost when the form returns with error messages. Consequently, users are required to re-upload the file, resulting in a less user-friendly experience.

To overcome the problem of losing file input value in simple cases, you can adopt the following approach:

Before:

::bad_form::

After:

::page submit my_form::

Form Restructuring: Move the binary file input outside the main form element in the HTML structure.

Using the form Attribute: Enhance the binary file input by adding the `form attribute` and setting its value to the ID of the main form. This linkage associates the binary file input with the form, even when it resides outside the form element.
"""
HEIGHT = "250px"
