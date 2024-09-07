from fasthtml.common import H3, Button, Div, Form, Hr, Input, Progress, Script, fast_app
from starlette.datastructures import UploadFile

app, rt = fast_app(hdrs=[Script(src="https://unpkg.com/hyperscript.org@0.9.12")])


@app.get
def page():
    return Div(
        Div(H3("Method 1: Pure JS"), Div(method1())),
        Hr(),
        Div(H3("Method 2: Hyperscript"), Div(method2())),
        cls="container",
    )


@app.get
def method1():
    js = """
    htmx.on('#form', 'htmx:xhr:progress', function(evt) {
        htmx.find('#progress').setAttribute('value', evt.detail.loaded/evt.detail.total * 100)
    });
    """
    form = Form(
        Input(type="file", name="file"),
        Button("Upload"),
        Progress(id="progress", value="0", max="100"),
        Div(id="output"),
        hx_target="#output",
        hx_post=upload.rt(),
        id="form",
    )
    return form, Script(js)


@app.get
def method2():
    return Form(
        Input(type="file", name="file"),
        Button("Upload"),
        Progress(id="progress2", value="0", max="100"),
        Div(id="output2"),
        hx_target="#output2",
        hx_encoding="multipart/form-data",
        hx_post=upload.rt(),
        _="on htmx:xhr:progress(loaded, total) set #progress2.value to (loaded/total)*100",
    )


@app.post
async def upload(file: UploadFile):
    # print(len(await file.read()))
    return Div(f"Uploaded! Filename: {file.filename}. Filesize: {file.size}")


DESC = "Demonstrates how to upload a file via ajax with a progress bar"
DOC = """
In this example we show how to create a file upload form that will be submitted via ajax, along with a progress bar.

We will show two different implementation, one in pure javascript (using some utility methods in htmx) and one in hyperscript

First the pure javascript version.

 - We have a form of type multipart/form-data so that the file will be properly encoded
 - We post the form to /upload
 - We have a progress element
 - We listen for the htmx:xhr:progress event and update the value attribute of the progress bar based on the loaded and total properties in the event detail.

::method1::

The Hyperscript version is very similar, except:

The script is embedded directly on the form element
Hyperscript offers nicer syntax (although the htmx API is pretty nice too!)
```python
app, rt = fast_app(hdrs=[Script(src="https://unpkg.com/hyperscript.org@0.9.12")])
```
::method2::

Note that hyperscript allows you to destructure properties from details directly into variables
"""
