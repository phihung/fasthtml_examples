from pathlib import Path

import httpx
import pytest
from starlette.testclient import TestClient

from tutorial import get_app, get_example

EXAMPLES = [f.stem for f in Path("src/tutorial").glob("*.py") if f.stem not in ["__init__"]]


@pytest.mark.parametrize("example", EXAMPLES)
def test_example_page(client, example):
    m = get_example(example)
    main_func = next(x for x in m.module.app.routes if m.start_url.endswith(x.path)).name

    r = client.get(f"/{m.slug}")
    assert r.status_code == 200
    assert m.module.DOC.strip().splitlines()[0] in r.text
    assert "::" not in r.text

    r = client.get(f"/{m.slug}?tab=code")
    assert r.status_code == 200
    assert m.module.DOC.strip().splitlines()[0] not in r.text
    assert f"def {main_func}" in r.text
    assert "app, rt = fast_app(" in r.text
    assert m.htmx_url in r.text
    assert httpx.head(m.htmx_url).status_code == 200


@pytest.mark.parametrize("example", EXAMPLES)
def test_start_url(client, example):
    m = get_example(example)
    r = client.get(m.start_url)
    assert r.status_code == 200
    print(r.text)
    assert "<html>" in r.text


@pytest.fixture
def client():
    return TestClient(get_app())
