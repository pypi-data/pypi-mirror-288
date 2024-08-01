import json
from importlib.resources import files
from urllib.parse import urlparse

from nbweb.page import Page
from nbweb.parser import Parser


def get_content(url: str):
    rules = get_rules(url)
    html = Page(url).get()
    content = Parser(rules, html).get()
    return content


def get_rules(url: str):
    u = urlparse(url)
    json_data = json.loads(files("nbweb").joinpath("data.json").read_text())
    for entry in json_data:
        e = urlparse(entry["url"])
        if u.hostname in e.hostname:
            return entry["rules"]
    raise TypeError("url not supported")
    return None
