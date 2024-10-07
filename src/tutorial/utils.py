import fasthtml.common as fh
from fasthtml.js import Script, jsd


def HighlightJS(
    sel="pre code",  # CSS selector for code elements. Default is industry standard, be careful before adjusting it
    langs: str | list | tuple = "python",  # Language(s) to highlight
    light="atom-one-light",  # Light theme
    dark="atom-one-dark",  # Dark theme
):
    "Implements browser-based syntax highlighting. Usage example [here](/tutorials/quickstart_for_web_devs.html#code-highlighting)."
    src = (
        """
// hljs.addPlugin(new CopyButtonPlugin());
hljs.configure({'cssSelector': '%s'});
htmx.onLoad(hljs.highlightAll);"""
        % sel
    )
    hjs = "highlightjs", "cdn-release", "build"
    # hjc = "arronhunt", "highlightjs-copy", "dist"
    if isinstance(langs, str):
        langs = [langs]
    langjs = [jsd(*hjs, f"languages/{lang}.min.js") for lang in langs]
    return [
        jsd(*hjs, f"styles/{dark}.css", typ="css", **{"x-bind:disabled": "darkMode !== 'dark'"}),
        jsd(*hjs, f"styles/{light}.css", typ="css", **{"x-bind:disabled": "darkMode !== 'light'"}),
        jsd(*hjs, "highlight.min.js"),
        # jsd(*hjc, "highlightjs-copy.min.js"),
        # jsd(*hjc, "highlightjs-copy.min.css", typ="css"),
        # fh.Style(".hljs-copy-button {background-color: #2d2b57;}", **{"x-bind:disabled": "darkMode !== 'light'"}),
        *langjs,
        Script(src, type="module"),
    ]


def alpine():
    return (
        fh.Script(src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js", defer=True),
        fh.Style("[x-cloak] {\n display: none !important; \n}"),
    )


def social_card():
    return fh.Socials(
        title="HTMX examples with FastHTML",
        description="Reproduction of HTMX official examples with Python FastHTML",
        site_name="phihung-htmx-examples.hf.space",
        twitter_site="@hunglp",
        image="/social.png",
        url="https://phihung-htmx-examples.hf.space",
    )


def concat(*elts, sep=" | "):
    out = [elts[0]]
    for elt in elts[1:]:
        out += [sep, elt]
    return out
