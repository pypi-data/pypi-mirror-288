from nbweb.page import Page


def test_failure() -> None:
    url = "https://subratlima.xyz"
    p = Page(url)
    html = p.get()
    assert html is None


def test_success() -> None:
    url = "https://httpbin.org"
    p = Page(url)
    html = p.get()
    assert html is not None


def monkeypatch_func(*kargs, **kwargs) -> None:
    return "one two three"


def test_load_from_cache(monkeypatch) -> None:
    url = "https://httpbin.org/get"
    p = Page(url)
    html = p.get()
    assert html is not None
    assert html != "one two three"

    monkeypatch.setattr(Page, "_fetch_from_cache", monkeypatch_func)
    p2 = Page(url)
    html = p2.get()

    assert html == "one two three"
