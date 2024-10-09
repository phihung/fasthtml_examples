from fasthtml.common import Div, fast_app, Script, Button, Label

js_solution_2 = """
document.addEventListener("htmx:confirm", function(e) {
    console.log(e);
    // The event is triggered on every trigger for a request, so we need to check if the element
    // that triggered the request has a hx-confirm attribute, if not we can return early and let
    // the default behavior happen
    if (!e.detail.target.hasAttribute('hx-confirm')) return

    // This will prevent the request from being issued to later manually issue it
    e.preventDefault()

    Swal.fire({
        title: "Proceed?",
        text: `I ask you... ${e.detail.question}`
    }).then(function(result) {
    if (result.isConfirmed) {
        // If the user confirms, we manually issue the request
        e.detail.issueRequest(true); // true to skip the built-in window.confirm()
    }
    })
})
"""

app, rt = fast_app(hdrs=[Script(src="https://cdn.jsdelivr.net/npm/sweetalert2@11"), Script(js_solution_2)])


@app.get
def page():
    return Div(cls="container grid")(Label("Solution 1"), solution1(), Label("Solution 2"), solution2())


# ---- Solution 1 ----
def solution1():
    js = """
    Swal.fire({title: 'Confirm', text:'Do you want to continue?'}).then((result)=>{
        if(result.isConfirmed){
            htmx.trigger(this, 'confirmed');  
        } 
    })
    """
    return Button("Click me", hx_get=confirmed, hx_trigger="confirmed", onClick=js)


@app.get
def confirmed():
    return "Confirmed"


# ---- Solution 2 ----


def solution2():
    return Button("Click me", hx_get=confirmed, hx_confirm="Do you want to continue?")


DESC = "Demonstrates how to implement a custom confirmation dialog with htmx"
DOC = """
htmx supports the [hx-confirm](https://htmx.org/attributes/hx-confirm/) attribute to provide a simple mechanism for confirming a user action. This uses the default confirm() function in javascript which, while trusty, may not be consistent with your applications UX.

In this example we will see how to use [sweetalert2](https://sweetalert2.github.io/) to implement a custom confirmation dialog. Below are two examples, one using a click+custom event method, and one using the built-in hx-confirm attribute and the [htmx:confirm](https://htmx.org/events/#htmx:confirm) event.

## Using on click+custom event
::solution1::

Here we use javascript to show a Sweet Alert 2 on a click, asking for confirmation. If the user confirms the dialog, we then trigger the request by triggering the custom “confirmed” event which is then picked up by hx-trigger.

## Vanilla JS, hx-confirm

We add some javascript to invoke Sweet Alert 2 on a click, asking for confirmation. If the user confirms the dialog, we trigger the request by calling the issueRequest method. We pass `skipConfirmation=true` as argument to skip `window.confirm`.

::solution2::
Javascript code

::js_solution_2::
This allows to use hx-confirm’s value in the prompt which is convenient when the question depends on the element.

Learn more about the htmx:confirm event [here](https://htmx.org/events/#htmx:confirm).
"""
HTMX_URL = "https://htmx.org/examples/confirm/"
HEIGHT = "250px"
