import os
import re

import httpx

HTML_DIR = ".cache/html"


class Page:
    def __init__(self, url: str) -> None:
        self.url = url
        self._set_folder()
        self._set_filename()

    def get(self) -> str:
        if os.path.exists(self.filepath):
            html = self._fetch_from_cache()
        else:
            html = self._fetch()
            if html is not None:
                self._save_to_cache(html)
        return html

    def _set_folder(self) -> None:
        if not os.path.exists(HTML_DIR):
            os.makedirs(HTML_DIR)

    def _set_filename(self) -> None:
        regex = r"^(https?://)?(?P<url>(?P<domain>[\w.]+)(/[\w.]+)*)"
        r = re.search(regex, self.url)
        self.filename = r.group("url").replace("/", "_")
        self.filepath = os.path.join(HTML_DIR, self.filename)

    def _fetch(self) -> str:
        try:
            r = httpx.get(self.url)
            r.raise_for_status()
        except httpx.HTTPError:
            return None
        return r.text

    def _fetch_from_cache(self) -> str:
        with open(self.filepath) as f:
            html = f.read()
        return html

    def _save_to_cache(self, html):
        with open(self.filepath, "w") as f:
            f.write(html)
