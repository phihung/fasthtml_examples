import inspect
import re
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from types import ModuleType

import fasthtml.common as fh
from fasthtml.common import H1, A, Code, Div, Hgroup, P, Pre

from tutorial import utils


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

    def create_routes(self, main_app: fh.FastHTML):
        sub_app, slug = self.module.app, self.slug
        self._fix_url()
        sub_app.htmlkw = main_app.htmlkw
        sub_app.hdrs.append(utils.alpine())
        main_app.mount(f"/{slug}", sub_app)
        main_app.get(f"/{slug}")(self.main_page)

    def main_page(self, tab: str = "explain"):
        module = self.module
        if tab == "code":
            code = Path(module.__file__).read_text().split("DESC = ")[0]
            code = code.strip().replace("# fmt: on\n", "").replace("# fmt: off\n", "")
            content = Pre(Code(code))
        else:
            doc = _replace_code_blocks(module, self.doc)
            content = Div(doc, cls="marked")

        return fh.Main(cls="container")(
            Hgroup(H1(self.title), P(self.desc)),
            Div(
                *utils.concat(
                    A("HOME", href="/"),
                    A("Explain", href=f"/{self.slug}?tab=explain"),
                    A("Code", href=f"/{self.slug}?tab=code"),
                    A("Htmx Docs", href=self.htmx_url),
                    A("Full screen", href=self.start_url),
                )
            ),
            Div(cls="grid")(
                Div(content, style="height:80vh;overflow:scroll"),
                Div(
                    fh.Iframe(src=self.start_url, height="500px", width="100%"),
                ),
            ),
        )

    def _fix_url(self):
        sub_app, slug = self.module.app, self.slug
        code = f"""
        document.addEventListener('htmx:configRequest', (event) => {{
            if (!event.detail.path.startsWith('/{slug}')) {{
                event.detail.path = `/{slug}${{event.detail.path}}`
            }}
        }})
        """
        sub_app.hdrs.append(fh.Script(code))


def _replace_code_blocks(module, doc):
    """Replace placeholders by real implementations"""
    return re.sub("::([a-zA-Z_0-9\s]+)::", lambda x: _code_block(module, x.group(1).strip().split()), doc)


def _code_block(module, function_names):
    code = ""
    for o in function_names:
        func = getattr(module, o)
        if callable(func):
            func = getattr(func, "__wrapped__", func)
            code += inspect.getsource(func)
        else:
            code += str(func).strip()
        code += "\n"
    code = code.strip()
    return f"```\n{code.strip()}\n```"
