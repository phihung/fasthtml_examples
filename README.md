---
title: Htmx Examples
emoji: 🦀
colorFrom: red
colorTo: green
sdk: docker
pinned: false
license: mit
app_port: 5001
---

# Fasthtml Examples

The repository reproduces HTMX official [examples](https://htmx.org/examples/) in Python with [FastHTML](https://docs.fastht.ml/)

Visit the site [here](https://phihung-htmx-examples.hf.space)

Github: [link](https://github.com/phihung/fasthtml_examples)

Run

```bash
# Local
uv run start_tutorial

# Docker
docker build -t htmx_examples .
docker run --rm -p 5001:5001 -it htmx_examples
```

## Dev

```bash
uv sync
uv run playwright install
uv run pytest
```
