import importlib
from pathlib import Path

import fasthtml.common as fh
from fasthtml.common import A, Div, Table, Tbody, Td, Th, Thead, Tr

from tutorial import utils
from tutorial.example import Example

hdrs = (
    fh.MarkdownJS(),
    utils.HighlightJS(langs=["python", "javascript", "html", "css"]),
    *fh.Socials(
        title="HTMX examples with FastHTML",
        description="Reproduction of HTMX official examples with Python FastHTML",
        site_name="phihung-htmx-examples.hf.space",
        twitter_site="@hunglp",
        image="/social.png",
        url="https://phihung-htmx-examples.hf.space",
    ),
    utils.alpine(),
)
html_kv = {
    "x-data": "{darkMode: localStorage.getItem('darkMode') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')}",
    "x-init": "$watch('darkMode', val => localStorage.setItem('darkMode', val))",
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
