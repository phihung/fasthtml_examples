from fasthtml.common import H3, Button, Div, HttpHeader, Style, fast_app

css = """
.progress {
    height: 20px;
    margin-bottom: 20px;
    overflow: hidden;
    background-color: #f5f5f5;
    border-radius: 4px;
    box-shadow: inset 0 1px 2px rgba(0,0,0,.1);
}
.progressbar {
    float: left;
    width: 0%;
    height: 100%;
    font-size: 12px;
    line-height: 20px;
    color: #fff;
    text-align: center;
    background-color: #337ab7;
    -webkit-box-shadow: inset 0 -1px 0 rgba(0,0,0,.15);
    box-shadow: inset 0 -1px 0 rgba(0,0,0,.15);
    -webkit-transition: width .6s ease;
    -o-transition: width .6s ease;
    transition: width .6s ease !important;
}
"""

app, rt = fast_app(hdrs=[Style(css)])

current = 1


@app.get
def page():
    return Div(hx_target="this", hx_swap="outerHTML")(
        H3("Start Progress"),
        Button("Start Job", hx_post=start, cls="btn primary"),
    )


@app.post
def start():
    global current
    current = 1
    return Div(hx_trigger="done", hx_get=job_finished, hx_swap="outerHTML", hx_target="this")(
        H3("Running", role="status", id="pblabel", tabindex="-1", autofocus=""),
        Div(hx_get=progress_bar, hx_trigger="every 600ms", hx_target="this", hx_swap="innerHTML")(
            progress_bar(),
        ),
    )


@app.get
def progress_bar():
    global current
    if current <= 100:
        current += 20
        return Div(cls="progress")(
            Div(style=f"width:{current - 20}%", id="THIS_ID_IS_INDISPENSIBLE", cls="progressbar"),
        )
    return HttpHeader("HX-Trigger", "done")


@app.get
def job_finished():
    return Div(hx_swap="outerHTML", hx_target="this")(
        H3("Complete", role="status", id="pblabel", tabindex="-1", autofocus=""),
        Div(Div(style="width:100%", id="THIS_ID_IS_INDISPENSIBLE", cls="progressbar"), cls="progress"),
        Button("Restart Job", hx_post=start, cls="btn primary show"),
    )


DESC = "Demonstrates a job-runner like progress bar"
DOC = """
This example shows how to implement a smoothly scrolling progress bar.

We start with an initial state with a button that issues a POST to /start to begin the job:
::page::
This progress bar is updated every 600 milliseconds, with the “width” style attribute and aria-valuenow attributed set to current progress value. Because there is an id on the progress bar div, htmx will smoothly transition between requests by settling the style attribute into its new value. This, when coupled with CSS transitions, makes the visual transition continuous rather than jumpy.
::start progress_bar::
Finally, when the process is complete, a server returns HX-Trigger: done header, which triggers an update of the UI to “Complete” state with a restart button added to the UI:
::job_finished::
"""
HEIGHT = "200px"
