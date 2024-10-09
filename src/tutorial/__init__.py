import importlib
import json
from dataclasses import dataclass
from pathlib import Path

import fasthtml.common as fh
from fasthtml.common import H4, A, Div, Pre, Table, Tbody, Td, Th, Thead, Tr

from tutorial import utils
from tutorial.example import Example

hdrs = (
    fh.MarkdownJS(),
    utils.HighlightJS(langs=["python", "javascript", "html", "css"]),
    utils.social_card(),
    utils.alpine(),
    fh.Script(src="/script.js"),
    fh.Script("init_main_page()"),
)
html_kv = {
    "x-data": """{
        showRequests: localStorage.getItem('showRequests') == 'true',
        darkMode: localStorage.getItem('darkMode') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
    }""",
    "x-init": "$watch('darkMode', val => localStorage.setItem('darkMode', val));$watch('showRequests', val => localStorage.setItem('showRequests', val))",
    "x-bind:data-theme": "darkMode !== 'system'? darkMode : (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')",
}

app, rt = fh.fast_app(hdrs=hdrs, static_path="public", htmlkw=html_kv, surreal=False)

htmx_examples = sorted([f.stem for f in Path(__file__).parent.glob("htmx/*.py") if f.stem not in ["__init__"]])
INTRO = """
# HTMX examples with FastHTML

Reproduction of HTMX official [examples](https://htmx.org/examples/) with Python [FastHTML](https://docs.fastht.ml/).

The code can be found on [GitHub](https://github.com/phihung/fasthtml_examples).
"""


@app.get("/")
def homepage():
    ls = [get_example(name) for name in htmx_examples]
    return (
        fh.Title("HTMX examples with FastHTML"),
        fh.Main(cls="container")(
            Div(INTRO, cls="marked"),
            Div(
                "Choose theme ",
                fh.Select(style="display:inline-block;max-width:100px;", **{"x-model": "darkMode"})(
                    fh.Option("Light", value="light"),
                    fh.Option("Dark", value="dark"),
                ),
            ),
            Table(
                Thead(Tr(Th("Pattern"), Th("Description"))),
                Tbody(tuple(Tr(Td(A(ex.title, href="/" + ex.slug)), Td(ex.desc)) for ex in ls)),
            ),
        ),
    )


@dataclass
class RequestInfo:
    verb: str
    path: str
    parameters: str
    headers: str
    response: str


@app.put("/requests")
def requests(r: RequestInfo):
    headers = json.loads(r.headers)
    print(headers)
    headers = {
        k: v for k, v in headers.items() if k in ("HX-Trigger", "HX-Trigger-Name", "HX-Target", "HX-Prompt") and v
    }
    return Div(**{"x-data": "{show: false}", "@click": "show = !show"})(
        H4(x_text="(show?'▽':'▶') + ' " + r.verb.upper() + " " + r.path + "'"),
        Div(**{"x-show": "show"})(
            Div(Pre("Input: " + r.parameters)) if r.parameters != "{}" else None,
            Div(Pre("Headers: " + str(headers))) if headers else None,
            Div(Pre(r.response or "(empty response)"), style="max-height:150px;overflow:scroll;"),
        ),
    )


def get_app():
    for name in htmx_examples:
        get_example(name).create_routes(app)
    return app


def get_example(name):
    module = importlib.import_module(f"tutorial.htmx.{name}")
    return Example(module, name[4:])


def start():
    fh.serve("tutorial.__init__", app="get_app")


if __name__ == "__main__":
    fh.serve(app="get_app")
