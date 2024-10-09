from fasthtml.common import H2, Button, Div, Form, Input, Link, Script, fast_app

app, rt = fast_app(
    hdrs=[
        Script(src="https://unpkg.com/hyperscript.org"),
        Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/uikit/3.5.9/css/uikit-core.min.css"),
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
            _="on htmx:afterOnLoad wait 10ms then add .uk-open to #modal",
        ),
        Div(id="modals-here"),
    )


@app.get
def modal():
    return Div(id="modal", cls="uk-modal", style="display:block;")(
        Div(cls="uk-modal-dialog uk-modal-body")(
            H2("Modal Dialog", cls="uk-modal-title"),
            Form(
                Div(cls="uk-margin")(Input(cls="uk-input", placeholder="What is Your Name?")),
                Button(
                    "Save Changes",
                    cls="uk-button uk-button-primary",
                    type="button",
                ),
                Button(
                    "Close",
                    id="cancelButton",
                    cls="uk-button uk-button-default",
                    type="button",
                    _="on click take .uk-open from #modal wait 200ms then remove #modal",
                ),
            ),
        )
    )


DESC = "Demonstrates modal dialogs using Bootstrap"
DOC = """
Many CSS toolkits include styles (and Javascript) for creating modal dialog boxes. This example shows how to use HTMX to display dynamic dialog using UIKit, and how to trigger its animation styles with little or no Javascript.

We start with a button that triggers the dialog, along with a DIV at the bottom of your markup where the dialog will be loaded:

This is an example of using HTMX to remotely load modal dialogs using UIKit. In this example we will use Hyperscript to demonstrate how cleanly that scripting language allows you to glue htmx and other libraries together.

::page::

This button uses a GET request to /modal when this button is clicked. The contents of this file will be added to the DOM underneath the #modals-here DIV.

Rather than using the standard UIKit Javascript library we are using a bit of Hyperscript, which triggers UIKit’s smooth animations. It is delayed by 10ms so that UIKit’s animations will run correctly.

Finally, the server responds with a slightly modified version of UIKit’s standard modal

::modal::

Hyperscript on the button and the form trigger animations when this dialog is completed or canceled. If you didn’t use this Hyperscript, the modals will still work but UIKit’s fade in animations will not be triggered.

You can, of course, use JavaScript rather than Hyperscript for this work, it’s just a lot more code:

```js
// This triggers the fade-in animation when a modal dialog is loaded and displayed
window.document.getElementById("showButton").addEventListener("htmx:afterOnLoad", function() {
	setTimeout(function(){
		window.document.getElementById("modal").classList.add("uk-open")
	}, 10)
})

// This triggers the fade-out animation when the modal is closed.
window.document.getElementById("cancelButton").addEventListener("click", function() {
	window.document.getElementById("modal").classList.remove("uk-open")
	setTimeout(function(){
		window.document.getElementById("modals-here").innerHTML = ""
		,200
	})
})
```
"""
HTMX_URL = "https://htmx.org/examples/modal-uikit/"
HEIGHT = "350px"
