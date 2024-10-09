from fasthtml.common import Div, fast_app, Button, Output, Script

js = """
// auth is a promise returned by our authentication system
const auth = new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve("super-dummy-token");
  }, 300);
});

// await the auth token and store it somewhere
let authToken = null;
auth.then((token) => {
    authToken = token
})

// gate htmx requests on the auth token
htmx.on("htmx:confirm", (e)=> {
    // if there is no auth token
    if(authToken == null) {
        // stop the regular request from being issued
        e.preventDefault() 
        // only issue it once the auth promise has resolved
        auth.then(() => e.detail.issueRequest()) 
    }
})

// add the auth token to the request as a header
htmx.on("htmx:configRequest", (e)=> {
    e.detail.headers["AUTH"] = authToken
})
"""

app, rt = fast_app(hdrs=[Script(js)])


@app.get
def page():
    return Div(cls="container grid")(
        Button("An htmx-Powered button", hx_post=example, hx_target="next output"), Output("--")
    )


@app.post
def example(request):
    return "Method call with token: " + request.headers["AUTH"]


DESC = "Demonstrates how to handle async authentication tokens in htmx"
DOC = """
This example shows how to implement an an async auth token flow for htmx.

The technique we will use here will take advantage of the fact that you can delay requests using the htmx:confirm event.

We first have a button that should not issue a request until an auth token has been retrieved:

::page example::
Next we will add some scripting to work with an auth promise (returned by a library):

::js::
Here we use a global variable, but you could use localStorage or whatever preferred mechanism you want to communicate the authentication token to the `htmx:configRequest` event.

With this code in place, htmx will not issue requests until the auth promise has been resolved.
"""
HEIGHT = "150px"
