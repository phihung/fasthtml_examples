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
.progress-bar {
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


@app.get("/page")
def main_page():
    return Div(
        H3("Start Progress"),
        Button("Start Job", hx_post="/start", cls="btn primary"),
        hx_target="this",
        hx_swap="outerHTML",
    )


@app.post("/start")
def start_job():
    global current
    current = 1
    return Div(
        H3("Running", role="status", id="pblabel", tabindex="-1", autofocus=""),
        Div(
            get_progress(),
            hx_get="/job/progress",
            hx_trigger="every 600ms",
            hx_target="this",
            hx_swap="innerHTML",
        ),
        hx_trigger="done",
        hx_get="/job",
        hx_swap="outerHTML",
        hx_target="this",
    )


@app.get("/job/progress")
def get_progress():
    global current
    if current <= 100:
        current += 10
        return Div(Div(style=f"width:{current - 10}%", cls="progress-bar"), cls="progress")
    return HttpHeader("HX-Trigger", "done")


@app.get("/job")
def view_completed():
    return Div(
        H3("Complete", role="status", id="pblabel", tabindex="-1", autofocus=""),
        Div(Div(style="width:100%", cls="progress-bar"), cls="progress"),
        Button("Restart Job", hx_post="/start", cls="btn primary show"),
        hx_swap="outerHTML",
        hx_target="this",
    )


DESC = "Demonstrates a job-runner like progress bar"
DOC = """
This example shows how to implement a smoothly scrolling progress bar.

We start with an initial state with a button that issues a POST to /start to begin the job:
::main_page::
This progress bar is updated every 600 milliseconds, with the “width” style attribute and aria-valuenow attributed set to current progress value. Because there is an id on the progress bar div, htmx will smoothly transition between requests by settling the style attribute into its new value. This, when coupled with CSS transitions, makes the visual transition continuous rather than jumpy.
::start_job get_progress::
Finally, when the process is complete, a server returns HX-Trigger: done header, which triggers an update of the UI to “Complete” state with a restart button added to the UI:
::view_completed::
"""
