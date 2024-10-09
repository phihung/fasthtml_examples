from fasthtml.common import Div, Label, Style, fast_app

css = """
.selected {
  color: rgb(16, 149, 193);
  cursor: pointer;
}
"""
app, rt = fast_app(hdrs=[Style(css)])

js = """
let currentTab = document.querySelector('.selected');
currentTab.classList.remove('selected')
let newTab = event.target
newTab.classList.add('selected')
"""


@app.get
def page():
    return (
        Div(hx_target="#tab_content", **{"hx-on:htmx-after-on-load": js}, style="display:flex;gap:15px")(
            Label("Tab 1", hx_get=tab1, cls="selected"),
            Label("Tab 2", hx_get=tab2, cls=""),
            Label("Tab 3", hx_get=tab3, cls=""),
        ),
        Div(hx_get=tab1, hx_trigger="load", id="tab_content"),
    )


@app.get
def tab1():
    return Div("This is the content of tab 1")


@app.get
def tab2():
    return Div("This is the content of tab 2")


@app.get
def tab3():
    return Div("This is the content of tab 3")


DESC = "Demonstrates how to display and select tabs using JavaScript"
DOC = """
This example shows how to load tab contents using htmx, and to select the “active” tab using Javascript. This reduces some duplication by offloading some of the work of re-rendering the tab HTML from your application server to your clients’ browsers.

You may also consider a more idiomatic approach that follows the principle of Hypertext As The Engine Of Application State.

The HTML below displays a list of tabs, with added HTMX to dynamically load each tab pane from the server.
::page::

A simple JavaScript event handler uses the take function to switch the selected tab when the content is swapped into the DOM.
::js::
"""
HTMX_URL = "https://htmx.org/examples/tabs-javascript/"
HEIGHT = "100px"
