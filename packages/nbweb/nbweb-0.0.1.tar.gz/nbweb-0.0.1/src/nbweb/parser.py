from parsel import Selector


class Parser:
    def __init__(self, rules, html: str) -> None:
        self.rules = rules
        self.html = html
        self.parser = Selector(text=html)

    def get(self):
        data = {}
        for key in self.rules:
            data[key] = self._get_content(self.rules[key]["selector"])
        return data

    def _get_content(self, selector: str) -> str:
        elems = self.parser.css(selector).getall()
        if elems is not None and len(elems) > 0:
            return "\n".join(elems)
        return ""
