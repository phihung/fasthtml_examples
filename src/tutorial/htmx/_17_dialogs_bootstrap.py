from fasthtml.common import H2, Button, Div, Link, Script, fast_app

app, rt = fast_app(
    hdrs=[
        Script(src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js"),
        Link(
            rel="stylesheet",
            href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.2.2/css/bootstrap.min.css",
        ),
    ],
    pico=False,
)


@app.get
def page():
    return Div()(
        Button(
            "Open Modal",
            hx_get=modal,
            hx_target="#modals-here",
            data_bs_toggle="modal",
            data_bs_target="#modals-here",
            cls="btn btn-primary",
        ),
        Div(id="modals-here", cls="modal modal-blur fade", style="display:none")(
            Div(cls="modal-dialog modal-lg modal-dialog-centered", role="document")(Div(cls="modal-content"))
        ),
    )


@app.get
def modal():
    return Div(cls="modal-dialog modal-dialog-centered")(
        Div(cls="modal-content")(
            Div(cls="modal-header")(H2("Modal title")),
            Div(cls="modal-body")("Modal body text goes here."),
            Div(cls="modal-footer")(Button("Close", cls="btn btn-secondary", data_bs_dismiss="modal")),
        )
    )


DESC = "Demonstrates modal dialogs using UIKit"
DOC = """
Many CSS toolkits include styles (and Javascript) for creating modal dialog boxes. This example shows how to use HTMX alongside original JavaScript provided by Bootstrap.

We start with a button that triggers the dialog, along with a DIV at the bottom of your markup where the dialog will be loaded:
::page::
This button uses a GET request to /modal when this button is clicked. The contents of this file will be added to the DOM underneath the #modals-here DIV.

The server responds with a slightly modified version of Bootstrap’s standard modal
::modal::
"""
HTMX_URL = "https://htmx.org/examples/modal-bootstrap/"
HEIGHT = "350px"
