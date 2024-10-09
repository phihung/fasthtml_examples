from fasthtml.common import H2, Button, Div, Hr, Link, Script, fast_app

app, rt = fast_app(
    hdrs=[
        Link(rel="stylesheet", href="/htmx_dialogs_custom.css"),
        Script(src="https://unpkg.com/hyperscript.org", defer=True),
    ],
    pico=False,
)


@app.get
def page():
    return Div()(
        Button("Open a Modal", hx_get=modal, hx_target="body", hx_swap="beforeend", cls="btn primary"),
    )


@app.get
def modal():
    return Div(id="modal", _="on closeModal add .closing then wait for animationend then remove me")(
        Div(cls="modal-underlay", _="on click trigger closeModal"),
        Div(cls="modal-content")(
            H2("Modal Dialog"),
            "This is the modal content. You can put anything here, like text, or a form, or an image.",
            Hr(),
            Button("Close", cls="btn danger", _="on click trigger closeModal"),
        ),
    )


DESC = "Demonstrates modal dialogs from scratch"
DOC = """
While htmx works great with dialogs built into CSS frameworks (like Bootstrap and UIKit), htmx also makes it easy to build modal dialogs from scratch. Here is a quick example of one way to build them.

### High Level Plan
We’re going to make a button that loads remote content from the server, then displays it in a modal dialog. The modal content will be added to the end of the <body> element, in a div named #modal.

In this demo we’ll define some nice animations in CSS, and then use some Hyperscript to remove the modals from the DOM when the user is done. Hyperscript is not required with htmx, but the two were designed to be used together and it is much nicer for writing async & event oriented code than JavaScript, which is why we chose it for this example.

Main Page
::page::

Modal HTML Fragment
::modal::

[Here](/htmx_dialogs_custom.css) is the css for this example.
"""
HTMX_URL = "https://htmx.org/examples/modal-custom/"
HEIGHT = "350px"
