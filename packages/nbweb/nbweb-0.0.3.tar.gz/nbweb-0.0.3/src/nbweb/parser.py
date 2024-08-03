from parsel import Selector


class Parser:
    def __init__(self, rules, html: str) -> None:
        self.rules = rules
        self.html = html
        self.parser = Selector(text=html)

    def get(self):
        data = {}
        if "prepare" in self.rules:
            self.parser = self.parser.css(self.rules["prepare"])
        for key in self.rules:
            if key == "prepare":
                continue
            if "selector" in self.rules[key]:
                data[key] = self._get_content_by_css(self.rules[key]["selector"])
            elif "jmespath" in self.rules[key]:
                data[key] = self._get_content_by_jmespath(self.rules[key]["jmespath"])
            else:
                raise TypeError("selector not found")
        return data

    def _get_content_by_css(self, selector: str) -> str:
        elems = self.parser.css(selector).getall()
        if elems is not None and len(elems) > 0:
            return "\n".join(elems)
        return ""

    def _get_content_by_jmespath(self, selector: str) -> str:
        print(f"selector: {selector}")
        print(f"parser: {self.parser}")
        elems = self.parser.jmespath(selector).getall()
        if elems is not None and len(elems) > 0:
            return "\n".join(elems)
        return ""
