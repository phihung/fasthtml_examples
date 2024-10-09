from fasthtml.common import fast_app, Div, Iframe, A, Figure, Label, Article


app, rt = fast_app()


@app.get
def page():
    return Div(
        Label("Feel free to change the page back and forth. The video will keep playing. Enjoy!"),
        Iframe(hx_preserve=True, id="rick-roll", **iframe_kv),
        Label("You are on page: /page1"),
        A("Go to page 2", hx_boost=True, hx_get=page2, hx_target="body"),
    )


@app.get
def page2():
    return Article(
        Label("Feel free to change the page back and forth. The video will keep playing. Enjoy!"),
        Figure(
            Iframe(hx_preserve=True, id="rick-roll", **iframe_kv),
        ),
        Label("You are on page: /page2"),
        A("Back to page 1", hx_boost=True, hx_get=page, hx_target="body"),
    )


iframe_kv = dict(
    src="https://www.youtube.com/embed/GFq6wH5JR2A",
    title="Rick Astley - Never Gonna Give You Up (Official Music Video)",
    frameborder="0",
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share",
    referrerpolicy="strict-origin-when-cross-origin",
    allowfullscreen="",
)


DESC = "htmx will use the experimental moveBefore() API for moving elements, if it is present."
DOC = """
This page demonstrates the use of the experimental [moveBefore()](https://github.com/whatwg/dom/issues/1255) DOM API available in Chrome Canary, which has been integrated into the hx-preserve attribute of htmx, if it is available.

## Getting Chrome Canary & Enabling moveBefore()
For the demo to work properly you will need to install Chrome Canary and enable the API:

Navigate to [chrome://flags](chrome://flags).
Enable “Atomic DOM move”.

htmx takes advantage of this API in the `hx-preserve` functionality if it is available, allowing you to mark an element as “preserved” and having all its state preserved as it moves between areas on the screen when new content is merged in. This is significantly better developer experience than current alternatives, such as morphing, which rely on the structure of the new page being “close enough” to not have to move things like video elements.

## Demo
The video continues to play after changing of pages

::page page2::

If you inspect the video below you will see that it is embedded in a div element. If you click the “Go to page 2” link, which is boosted, you will transition to another page with a video element with the same id, but embedded in a figure element instead. Without the moveBefore() functionality it is impossible to keep the video playing in this situation because “reparenting” (i.e. changing the parent of an element) causes it to reset.

moveBefore() opens up a huge number of possibilities in web development by allowing developers to completely change the layout of a page while still preserving elements play state, focus, etc.
"""
HEIGHT = "300px"
