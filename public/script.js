function init_sub_page(slug) {
  console.log(`init_sub_page ${slug}`);
  document.addEventListener("htmx:configRequest", (event) => {
    if (!event.detail.path.startsWith(`/${slug}`)) {
      event.detail.path = `/${slug}${event.detail.path}`;
    }
  });

  document.addEventListener("htmx:afterRequest", (event) => {
    let req = event.detail.requestConfig;
    let detail = {
      verb: req.verb,
      path: req.path.slice(slug.length + 1),
      parameters: Object.fromEntries(req.formData),
      headers: req.headers,
      response: event.detail.xhr.response,
    };
    window.parent.document.dispatchEvent(
      new CustomEvent("SubappAfterRequest", { detail })
    );
  });
}

function init_main_page() {
  console.log("init_main_page");
  window.document.addEventListener(
    "SubappAfterRequest",
    (e) => {
      // console.log(e);
      htmx.ajax("PUT", "/requests", {
        target: "#request-list",
        values: e.detail,
        swap: "afterbegin",
      });
    },
    false
  );
}
