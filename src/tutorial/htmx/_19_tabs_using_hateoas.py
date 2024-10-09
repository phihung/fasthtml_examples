from fasthtml.common import Br, Div, Label, Style, fast_app

css = """
.selected {
  color: rgb(16, 149, 193);
  cursor: pointer;
}
"""
app, rt = fast_app(hdrs=[Style(css)])


@app.get
def page():
    return Div(hx_get=tab1, hx_trigger="load delay:100ms", hx_target="this")


@app.get
def tab1():
    return make_tab(1)


@app.get
def tab2():
    return make_tab(2)


@app.get
def tab3():
    return make_tab(3)


def make_tab(idx: int):
    return (
        Div(style="display:flex;gap:15px")(
            Label("Tab 1", hx_get=tab1, cls="selected" if idx == 1 else None),
            Label("Tab 2", hx_get=tab2, cls="selected" if idx == 2 else None),
            Label("Tab 3", hx_get=tab3, cls="selected" if idx == 3 else None),
        ),
        Div(f"This is the content of tab {idx}", Br(), str(idx) * 10),
    )


DESC = "Demonstrates how to display and select tabs using HATEOAS principles"
DOC = """
This example shows how easy it is to implement tabs using htmx. Following the principle of Hypertext As The Engine Of Application State, the selected tab is a part of the application state. Therefore, to display and select tabs in your application, simply include the tab markup in the returned HTML. If this does not suit your application server design, you can also use a little bit of JavaScript to select tabs instead.

The main page simply includes the following HTML to load the initial tab into the DOM.
::page::
Subsequent tab pages display all tabs and highlight the selected one accordingly.
::tab1 make_tab::
"""
HTMX_URL = "https://htmx.org/examples/tabs-hateoas/"
HEIGHT = "100px"
