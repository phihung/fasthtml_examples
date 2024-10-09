import time
from fasthtml.common import Article, Div, Form, Input, SortableJS, fast_app

app, rt = fast_app(hdrs=[SortableJS()])


@app.get
def page():
    return (
        Form(cls="sortable", hx_post="/items", hx_target="#logs", hx_trigger="end")(
            Div(cls="htmx-indicator")("Updating..."),
            *[Article(Input(type="hidden", name="item", value=i), f"Item {i}") for i in range(1, 6)],
        ),
        Div(id="logs"),
    )


@app.post
def items(item: list[str]):
    time.sleep(0.5)
    return f"Order: {', '.join(item)}"


DESC = "Demonstrates how to use htmx with the Sortable.js plugin to implement drag-and-drop reordering"
DOC = """
In this example we show how to integrate the Sortable javascript library with htmx.

To begin we initialize the `.sortable` class with the Sortable javascript library.
This is done automatically by fasthtml SortableJS implementation.

```python
app, rt = fast_app(hdrs=[SortableJS()])
```
Next, we create a form that has some sortable divs within it, and we trigger an ajax request on the end event, fired by Sortable.js:

::page::
Note that each div has a hidden input inside of it that specifies the item id for that row.
When the list is reordered via the Sortable.js drag-and-drop, the end event will be fired. htmx will then post the item ids in the new order to /items, to be persisted by the server.
That’s it!

If you do not use fasthtml SortableJS implementation, you can add the following script to your headers:

<details>
<summary role="button">If you do not use fasthtml SortableJS</summary>

```javascript
htmx.onLoad(function(content) {
    var sortables = content.querySelectorAll(".sortable");
    for (var i = 0; i < sortables.length; i++) {
      var sortable = sortables[i];
      var sortableInstance = new Sortable(sortable, {
          animation: 150,
          ghostClass: 'blue-background-class',

          // Make the `.htmx-indicator` unsortable
          filter: ".htmx-indicator",
          onMove: function (evt) {
            return evt.related.className.indexOf('htmx-indicator') === -1;
          },

          // Disable sorting on the `end` event
          onEnd: function (evt) {
            this.option("disabled", true);
          }
      });

      // Re-enable sorting on the `htmx:afterSwap` event
      sortable.addEventListener("htmx:afterSwap", function() {
        sortableInstance.option("disabled", false);
      });
    }
})
```
</details>
"""
# HEIGHT = "100px"
