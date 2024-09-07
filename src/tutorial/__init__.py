import importlib
import inspect
import re
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from types import ModuleType

from fasthtml.common import (
    H1,
    A,
    Code,
    Div,
    Hgroup,
    HighlightJS,
    Iframe,
    Main,
    MarkdownJS,
    P,
    Pre,
    Script,
    Table,
    Tbody,
    Td,
    Th,
    Thead,
    Tr,
    fast_app,
    serve,
)

hdrs = (
    MarkdownJS(),
    HighlightJS(langs=["python", "javascript", "html", "css"]),
)
app, rt = fast_app(hdrs=hdrs, static_path="public")

examples = sorted([f.stem for f in Path(__file__).parent.glob("*.py") if f.stem not in ["__init__"]])


INTRO = """
# HTMX examples with FastHTML

Reproduction of HTMX official [examples](https://htmx.org/examples/) with Python [FastHTML](https://docs.fastht.ml/).

The code can be found on [GitHub](https://github.com/phihung/fasthtml_examples).
"""


@app.get("/")
def homepage():
    ls = [get_example(name) for name in examples]
    return Main(cls="container")(
        Div(INTRO, cls="marked"),
        Table(
            Thead(Tr(Th("Pattern"), Th("Description"))),
            Tbody(tuple(Tr(Td(A(ex.title, href="/" + ex.slug)), Td(ex.desc)) for ex in ls)),
        ),
    )


def get_app():
    for name in examples:
        get_example(name).create_routes(app)
    return app


def get_example(name):
    module = importlib.import_module(f"tutorial.{name}")
    return Example(module, name[4:])


@dataclass
class Example:
    module: ModuleType
    name: str

    @cached_property
    def title(self):
        return self.name.replace("_", " ").title()

    @cached_property
    def desc(self):
        return self.module.DESC

    @cached_property
    def doc(self):
        return self.module.DOC

    @cached_property
    def slug(self):
        return self.name.replace("_", "-")

    @cached_property
    def htmx_url(self):
        return getattr(self.module, "HTMX_URL", f"https://htmx.org/examples/{self.slug}/")

    @cached_property
    def start_url(self):
        module, slug = self.module, self.slug
        url = getattr(module, "START_URL", module.app.routes[1].path)
        return f"/{slug}{url}"

    def create_routes(self, app):
        module, slug = self.module, self.slug
        self._fix_url()
        app.mount(f"/{slug}", module.app)
        app.get(f"/{slug}")(self.main_page)

    def main_page(self, tab: str = "explain"):
        module = self.module
        if tab == "code":
            code = Path(module.__file__).read_text().split("DESC = ")[0]
            code = code.strip().replace("# fmt: on\n", "").replace("# fmt: off\n", "")
            content = Pre(Code(code))
        else:
            doc = re.sub("::([a-zA-Z_0-9\s]+)::", lambda x: code_block(module, x.group(1)), self.doc)
            content = Div(doc, cls="marked")

        return Main(cls="container")(
            Hgroup(H1(self.title), P(self.desc)),
            Div(
                A("Back", href="/"),
                "|",
                A("Explain", href=f"/{self.slug}?tab=explain"),
                "|",
                A("Code", href=f"/{self.slug}?tab=code"),
                "|",
                A("Htmx Docs", href=self.htmx_url),
            ),
            Div(cls="grid")(
                Div(content, style="height:80vh;overflow:scroll"),
                Div(P(A("Direct url", href=self.start_url)), Iframe(src=self.start_url, height="500px", width="100%")),
            ),
        )

    def _fix_url(self):
        module, slug = self.module, self.slug
        code = f"""
        document.addEventListener('htmx:configRequest', (event) => {{
            event.detail.path = `/{slug}${{event.detail.path}}`
        }})
        """
        module.app.hdrs.append(Script(code))


def code_block(module, obj):
    code = ""
    for o in obj.strip().split():
        func = getattr(module, o)
        if callable(func):
            func = getattr(func, "__wrapped__", func)
            code += inspect.getsource(func)
        else:
            code += str(func).strip()
        code += "\n"
    code = code.strip()
    return f"```\n{code.strip()}\n```"


def start():
    serve("tutorial.__init__", app="get_app")


if __name__ == "__main__":
    serve(app="get_app")
