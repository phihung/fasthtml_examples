import time

from fasthtml.common import Button, Div, Form, Hr, Input, Script, Style, fast_app

css_demo1 = """
.smooth {
  transition: all 1s ease-in !important;
}
"""
css_demo2 = """
.fade-me-out.htmx-swapping {
  transition: opacity 2s ease-out !important;
  opacity: 0;
}
"""
css_demo3 = """
#demo3.htmx-added {
  opacity: 0;
}
#demo3 {
  opacity: 1;
  transition: opacity 1s ease-out !important;
}
"""
css_demo4 = """
form.htmx-request {
    opacity: .5;
    transition: opacity 300ms linear !important;
}
"""
css_demo5 = """
.demo5.faded {
    opacity:.3;
}
.demo5 {
    opacity:1;
    transition: opacity ease-in 900ms !important;
}
"""

app, rt = fast_app(
    hdrs=[
        Style(css_demo1 + css_demo2 + css_demo3 + css_demo4 + css_demo5),
        Script(src="https://unpkg.com/htmx-ext-class-tools@2.0.1/class-tools.js"),
    ],
    pico=False,
)


@app.get
def page():
    return Div(
        Div(Div("Example 1: Color Swap"), demo1()),
        Hr(),
        Div(Div("Example 2: Fade Out On Swap"), demo2()),
        Hr(),
        Div(Div("Example 3: Fade In On Addition"), demo3()),
        Hr(),
        Div(Div("Example 4: Request In Flight Animation"), demo4()),
        Hr(),
        Div(Div("Example 5: Class-tools Extension"), demo5()),
        cls="container",
    )


@app.get
def demo1(idx: int = 0):
    palette = ["red", "blue", "green", "orange"]
    next_idx = (idx + 1) % len(palette)
    return Div(
        "Color Swap Demo",
        id="color-demo",
        style=f"color:{palette[idx]}",
        hx_get=demo1.rt(idx=next_idx),
        hx_swap="outerHTML",
        hx_trigger="every 1s",
        cls="smooth",
    )


@app.get
def demo2():
    return Button("Fade Me Out", cls="fade-me-out", hx_delete=demo2_delete.rt(), hx_swap="outerHTML swap:2s")


@app.delete
def demo2_delete():
    return None


@app.get
def demo3():
    return Button("Fade Me In", hx_get=demo3.rt(), hx_swap="outerHTML settle:1s", id="demo3")


@app.get
def demo4():
    return Form(hx_post=demo4_form.rt(), hx_swap="outerHTML")(
        Input(name="name", placeholder="Your name here..."), Button("Submit", cls="btn primary")
    )


@app.post
def demo4_form():
    time.sleep(1)
    return Div("Submitted!")


@app.get
def demo5():
    return Div(Div("Toggle Demo", cls="demo5", classes="toggle faded:1s"), hx_ext="class-tools")


DESC = "Demonstrates making the values of a select dependent on another select"
HTMX_URL = "https://htmx.org/examples/value-select/"
DOC = """
htmx is designed to allow you to use CSS transitions to add smooth animations and transitions to your web page using only CSS and HTML. Below are a few examples of various animation techniques.

htmx also allows you to use the new View Transitions API for creating animations.

<blockquote>
We have to use <code>!important</code> in css to bypass <code>(prefers-reduced-motion: reduce)</code> setup by picocss
</blockquote>

### Basic CSS Animations

#### Color Throb
The simplest animation technique in htmx is to keep the id of an element stable across a content swap. If the id of an element is kept stable, htmx will swap it in such a way that CSS transitions can be written between the old version of the element and the new one.

Consider this div:
::css_demo1 demo1::

This div will poll every second and will get replaced with new content which changes the color style to a new value (e.g. blue):

Because the div has a stable id, color-demo, htmx will structure the swap such that a CSS transition, defined on the .smooth class, applies to the style update from red to blue, and smoothly transitions between them.

Color Swap Demo
#### Smooth Progress Bar
The [Progress Bar demo](/progress-bar) uses this basic CSS animation technique as well, by updating the length property of a progress bar element, allowing for a smooth animation.

### Swap Transitions
#### Fade Out On Swap
If you want to fade out an element that is going to be removed when the request ends, you want to take advantage of the htmx-swapping class with some CSS and extend the swap phase to be long enough for your animation to complete. This can be done like so:
::css_demo2 demo2 demo2_delete::

### Settling Transitions
#### Fade In On Addition
Building on the last example, we can fade in the new content by using the htmx-added class during the settle phase. You can also write CSS transitions against the target, rather than the new content, by using the htmx-settling class.
::css_demo3 demo3::

### Request In Flight Animation
You can also take advantage of the htmx-request class, which is applied to the element that triggers a request. Below is a form that on submit will change its look to indicate that a request is being processed:
::css_demo4 demo4::

### Using the htmx class-tools Extension
Many interesting animations can be created by using the [class-tools](https://github.com/bigskysoftware/htmx-extensions/blob/main/src/class-tools/README.md) extension.

Here is an example that toggles the opacity of a div. Note that we set the toggle time to be a bit longer than the transition time. This avoids flickering that can happen if the transition is interrupted by a class change.
::css_demo5 demo5::

#### Using the View Transition API
TODO

### Conclusion
You can use the techniques above to create quite a few interesting and pleasing effects with plain old HTML while using htmx.
"""
