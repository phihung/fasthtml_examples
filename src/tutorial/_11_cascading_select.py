import time

from fasthtml.common import H3, Div, Form, Img, Label, Option, Select, fast_app

app, rt = fast_app()


@app.get("/page")
def main_page():
    return Div(
        H3("Pick A Make/Model"),
        Form(
            Div(
                Label("Make"),
                Select(
                    Option("Audi", value="audi"),
                    Option("Toyota", value="toyota"),
                    Option("BMW", value="bmw"),
                    name="make",
                    hx_get="/models?sleep=1",
                    hx_target="#models",
                    hx_indicator=".htmx-indicator",
                ),
            ),
            Div(
                Label("Model"),
                Select(load_models("audi"), id="models"),
                Img(width="20", src="/img/bars.svg", cls="htmx-indicator"),
            ),
        ),
        cls="container",
    )


@app.get("/models")
def load_models(make: str, sleep: int = 0):
    time.sleep(sleep)
    cars = {
        "audi": ["A1", "A4", "A6"],
        "toyota": ["Landcruiser", "Tacoma", "Yaris"],
        "bmw": ["325i", "325ix", "X5"],
    }
    return tuple(Option(v, value=v) for v in cars[make])


DESC = "Demonstrates making the values of a select dependent on another select"
HTMX_URL = "https://htmx.org/examples/value-select/"
DOC = """
In this example we show how to make the values in one select depend on the value selected in another select.

To begin we start with a default value for the make select: Audi. We render the model select for this make. We then have the make select trigger a GET to /models to retrieve the models options and target the models select.

Here is the code:
::main_page::

When a request is made to the /models end point, we return the models for that make:
::load_models::

And they become available in the model select.
"""
