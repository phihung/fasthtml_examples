import time

from playwright.sync_api import Page


def test_end_to_end(page: Page):
    page.goto("/progress-bar/page")
    page.click("text=Start Job")
    w1, w2 = _get_widths(page)
    assert w1 < 0.1 * w2

    time.sleep(2)
    w1, w2 = _get_widths(page)
    assert w2 > w1 > 0.3 * w2

    time.sleep(1)
    page.click("text=Restart Job")
    time.sleep(1)
    assert w2 > w1 > 0.2 * w2


def _get_widths(page):
    return _get_width(page.locator(".progressbar")), _get_width(page.locator(".progress"))


def _get_width(el):
    return float(el.evaluate("el => window.getComputedStyle(el).width").replace("px", ""))
