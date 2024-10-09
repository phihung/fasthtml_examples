from fasthtml.common import Button, fast_app

app, rt = fast_app()


# <button class="btn primary" hx-trigger="click, keyup[altKey&&shiftKey&&key=='D'] from:body"
#         hx-post="/doit">Do It! (alt-shift-D)</button>
@app.get
def page():
    return Button("Do It! (shift-D)", hx_trigger="click, keyup[shiftKey&&key=='D'] from:body", hx_post="/doit")


@app.post
def doit():
    return "You did it!"


DESC = "Demonstrates how to create keyboard shortcuts for htmx enabled elements"
DOC = """
In this example we show how to create a keyboard shortcut for an action.

We start with a simple button that loads some content from the server:
::page::
Note that the button responds to both the click event (as usual) and also the keyup event when shift-D is pressed. The from: modifier is used to listen for the keyup event on the body element, thus making it a “global” keyboard shortcut.

You can trigger the demo below by either clicking on the button, or by hitting shift-D.

You can find out the conditions needed for a given keyboard shortcut here:

https://javascript.info/keyboard-events
"""
HEIGHT = "100px"
