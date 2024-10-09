# fmt: off
from fasthtml.common import H3, Div, Form, Input, Label, Script, Style, Table, Tbody, Td, Th, Thead, Tr, fast_app
# fmt: on

css = """
.selected {
  color: rgb(16, 149, 193);
  cursor: pointer;
}
"""
app, rt = fast_app(hdrs=[Style(css)])

data = [
    ("phi", "phi@example.com"),
    ("grace", "grace@example.com"),
]


@app.get
def page():
    return Div(cls="container")(
        Div(hx_get=solution.rt(idx=1), hx_trigger="load delay:100ms", hx_target="this", hx_swap="innerHTML")
    )


@app.get
def solution(idx: int):
    return Div(
        Div(
            Div(style="display:flex;gap:15px")(
                Label("Solution 1", hx_get=solution.rt(idx=1), cls="selected" if idx == 1 else None),
                Label("Solution 2", hx_get=solution.rt(idx=2), cls="selected" if idx == 2 else None),
                Label("Solution 3", hx_get=solution.rt(idx=3), cls="selected" if idx == 3 else None),
                Label("Solution 4", hx_get=solution.rt(idx=4), cls="selected" if idx == 4 else None),
            ),
        ),
        Div(
            H3(f"Solution {idx}"),
            [solution1, solution2, solution3, solution4][idx - 1](),
        ),
    )


# ---- Solution 1 ----


def solution1():
    return Div(hx_target="this")(
        Table(
            Thead(Tr(Th("Name"), Th("Email"), Th())),
            Tbody(*[Tr(Td(d) for d in row) for row in data]),
        ),
        Form(form_fields(), hx_post=solution1_add_contact, hx_swap="outerHTML"),
    )


@app.post("/solution1/contacts")
def solution1_add_contact(name: str, email: str):
    add_contact(name, email)
    return solution1()


# ---- Solution 2 ----


def solution2():
    return Div()(
        Table(
            Thead(Tr(Th("Name"), Th("Email"), Th())),
            Tbody(id="table")(*[Tr(Td(d) for d in row) for row in data]),
        ),
        Form(form_fields(), hx_post=solution2_add_contact, hx_target="this"),
    )


@app.post("/solution2/contacts")
def solution2_add_contact(name: str, email: str):
    add_contact(name, email)
    return (
        Tbody(hx_swap_oob="beforeend:#table")(Tr(Td(name), Td(email))),
        form_fields(),
    )


# ---- Solution 3 ----


def solution3():
    return Div()(
        Div(
            Table(
                Thead(Tr(Th("Name"), Th("Email"), Th())),
                Tbody(id="table", hx_get=solution3_contacts_table, hx_trigger="newContact from:body", hx_target="this")(
                    *[Tr(Td(d) for d in row) for row in data]
                ),
            ),
        ),
        Form(form_fields(), hx_post=solution3_add_contact, hx_target="this"),
    )


@app.get("/solution3/contacts/table")
def solution3_contacts_table():
    return [Tr(Td(d) for d in row) for row in data]


@app.post("/solution3/contacts")
def solution3_add_contact(name: str, email: str):
    add_contact(name, email)
    return (
        form_fields(),
        Script("htmx.trigger('body', 'newContact')"),
    )


# ---- Solution 4 ----


def solution4():
    return (
        Script(src="https://unpkg.com/htmx-ext-path-deps@2.0.0/path-deps.js"),
        Div(hx_ext="path-deps")(
            Table(
                Thead(Tr(Th("Name"), Th("Email"), Th())),
                Tbody(
                    hx_get=solution4_contacts_table,
                    hx_trigger="path-deps",
                    path_deps="/update-other-content/solution4/contacts",
                    hx_target="this",
                )(*[Tr(Td(d) for d in row) for row in data]),
            ),
            Form(form_fields(), hx_post=solution4_add_contact, hx_target="this"),
        ),
    )


@app.get("/solution4/contacts/table")
def solution4_contacts_table():
    return [Tr(Td(d) for d in row) for row in data]


@app.post("/solution4/contacts")
def solution4_add_contact(name: str, email: str):
    add_contact(name, email)
    return form_fields()


# ---- Utilities ----


def form_fields():
    return Div(style="display:flex;gap:5px")(
        Label("Name", Input(name="name")), Label("Email", Input(name="email")), Input(type="submit", hidden=True)
    )


def add_contact(name, email):
    global data
    data.append([name, email])
    data = data[-5:]


DESC = "Demonstrates how to update content beyond just the target elements"
DOC = """
A question that often comes up when people are first working with htmx is:
> I need to update other content on the screen. How do I do this?

There are multiple ways to do so, and in this example we will walk you through some of them.

We’ll use the following basic UI to discuss this concept: a simple table of contacts, and a form below it to add new contacts to the table using hx-post.

The problem here is that when you submit a new contact in the form, you want the contact table above to refresh and include the contact that was just added by the form.

What solutions do we have?

## Solution 1: Expand the Target

The easiest solution here is to “expand the target” of the form to enclose both the table and the form. For example, you could wrap the whole thing in a div and then target that div in the form:
::solution1 solution1_add_contact::

Note that we are targeting the enclosing div using the hx-target attribute. You would need to render both the table and the form in the response to the POST to /contacts.

This is a simple and reliable approach, although it might not feel particularly elegant.

## Solution 2: Out of Band Responses

A more sophisticated approach to this problem would use out of band swaps to swap in updated content to the DOM.

Using this approach, the HTML doesn’t need to change from the original setup at all:

::solution2::

Instead of modifying something on the front end, in your response to the POST to /contacts you would include some additional content:

::solution2_add_contact::

This content uses the [hx-swap-oob](https://htmx.org/attributes/hx-swap-oob/) attribute to append itself to the #table, updating the table after a contact is added successfully.

## Solution 3: Triggering Events

An even more sophisticated approach would be to trigger a client side event when a successful contact is created and then listen for that event on the table, causing the table to refresh.

::solution3::

We have added a new end-point `/contacts/table` that re-renders the contacts table. Our trigger for this request is a custom event, newContact. We listen for this event on the body because when it is triggered by the response to the form, it will end up hitting the body due to event bubbling.

::solution3_contacts_table::

When a successful contact creation occurs during a POST to `/contacts`, the response includes an `HX-Trigger` response header that looks like this:

::solution3_add_contact::

`HX-Trigger:newContact`
This will trigger the table to issue a GET to `/contacts/table` and this will render the newly added contact row
(in addition to the rest of the table.)

Very clean, event driven programming!

## Solution 4: Using the Path Dependencies Extension

A final approach is to use REST-ful path dependencies to refresh the table. Intercooler.js, the predecessor to htmx, had path-based dependencies integrated into the library.

htmx dropped this as a core feature, but supports an extension, [path deps](https://github.com/bigskysoftware/htmx-extensions/blob/main/src/path-deps/README.md), that gives you similar functionality.

Updating our example to use the extension would involve loading the extension javascript and then annotating our HTML like so:

::solution4 solution4_add_contact::
Now, when the form posts to the /contacts URL, the path-deps extension will detect that and trigger an path-deps event on the contacts table, therefore triggering a request.

The advantage here is that you don’t need to do anything fancy with response headers. The downside is that a request will be issued on every POST, even if a contact was not successfully created.

## Which should I use?
Generally I would recommend the first approach, expanding your target, especially if the elements that need to be updated are reasonably close to one another in the DOM. It is simple and reliable.

After that, I would say it is a tossup between the custom event and an OOB swap approaches. I would lean towards the custom event approach because I like event-oriented systems, but that’s a personal preference. Which one you choose should be dictated by your own software engineering tastes and which of the two matches up better with your server side technology of choice.

Finally, the path-deps approach is interesting, and if it fits well with your mental model and overall system architecture, it can be a fun way to avoid explicit refreshing. I would look at it last, however, unless the concept really grabs you.
"""
HEIGHT = "400px"
