from fasthtml.common import Button, Div, fast_app

app, rt = fast_app()


@app.get
def page():
    return Div()(
        Button(
            "Prompt Submission",
            hx_post=submit,
            hx_prompt="Enter a string",
            hx_confirm="Are you sure?",
            hx_target="#response",
        ),
        Div(id="response"),
    )


@app.post("/submit")
def submit(request, htmx: dict):
    return f"User entered <i>{request.headers['HX-Prompt']}</i>"


DESC = "Demonstrates the prompt and confirm dialogs"
DOC = """
Dialogs can be triggered with the hx-prompt and hx-confirmattributes. These are triggered by the user interaction that would trigger the AJAX request, but the request is only sent if the dialog is accepted.

::page submit::
The value provided by the user to the prompt dialog is sent to the server in a HX-Prompt header. In this case, the server simply echos the user input back.

```
User entered <i>${response}</i>
```
"""
HEIGHT = "100px"
HTMX_URL = "https://htmx.org/examples/dialogs/"
