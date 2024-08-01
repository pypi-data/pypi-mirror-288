from nbweb.parser import Parser


def test_parser() -> None:
    html = """
    <html>
        <body>
            <h1>dummy title</h1>
            <div class="article-content">
                <p>line 1</p>
                <p>line 2</p>
            </div>
            <img data-src="dummy-src">
        </body>
    </html>"""
    rules = {
        "title": {"selector": "h1::text"},
        "img": {"selector": "img::attr(data-src)"},
        "content": {"selector": "div.article-content > p::text"},
    }
    p = Parser(rules, html)
    data = p.get()

    assert data is not None
    assert len(data) == 3
    assert "title" in data
    assert "content" in data
    assert data["title"] == "dummy title"
    assert data["content"] == "line 1\nline 2"
    assert data["img"] == "dummy-src"
