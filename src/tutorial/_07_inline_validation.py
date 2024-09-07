import time

from fasthtml.common import H3, Button, Div, Form, Img, Input, Label, NotStr, Span, Style, fast_app

css = """
.error input {
    box-shadow: 0 0 3px #CC0000;
}
.valid input {
    box-shadow: 0 0 3px #36cc00;
}
"""

app, rt = fast_app(hdrs=[Style(css)])


@app.get
def page():
    return Div(
        H3("Signup Form"),
        NotStr(
            "Enter an email into the input below and on tab out it will be validated. Only <ins>test@test.com</ins> will pass."
        ),
        Form(
            make_email_field("", error=False, touched=False),
            Div(Label("Name"), Input(name="name")),
            Button("Submit", disabled="", cls="btn primary"),
        ),
        cls="container",
    )


@app.post("/contact/email")
def validate_email(email: str):
    time.sleep(2)
    return make_email_field(email, email != "test@test.com", True)


def make_email_field(value: str, error: bool, touched: bool):
    return Div(
        Label("Email"),
        Input(name="email", hx_post=validate_email.rt(), hx_indicator="#ind", value=value),
        Img(id="ind", src="/img/bars.svg", cls="htmx-indicator"),
        Span("Please enter a valid email address", style="color:red;") if error else None,
        hx_target="this",
        hx_swap="outerHTML",
        cls="" if not touched else "error" if error else "valid",
    )


DESC = "Demonstrates how to do inline field validation"
DOC = """
This example shows how to do inline field validation, in this case of an email address. To do this we need to create a form with an input that POSTs back to the server with the value to be validated and updates the DOM with the validation results.

We start with this form:
::page make_email_field::

Note that the email div in the form has set itself as the target of the request and specified the outerHTML swap strategy, so it will be replaced entirely by the response. The input then specifies that it will POST to /contact/email for validation, when the changed event occurs (this is the default for inputs). It also specifies an indicator for the request.

When a request occurs, it will return a partial to replace the outer div. It might look like this:

This form can be lightly styled with this CSS to give better visual feedback.
::css::
"""
