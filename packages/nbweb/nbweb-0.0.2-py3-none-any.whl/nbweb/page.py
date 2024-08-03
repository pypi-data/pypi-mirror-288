import os
import re

import httpx

from fake_useragent import UserAgent

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
        regex = r"^(https?://)?(?P<url>(?P<domain>[\w.]+)(/[\w.-_]+)*)"
        r = re.search(regex, self.url)
        self.filename = r.group("url").replace("/", "_").strip()
        self.filepath = os.path.join(HTML_DIR, self.filename)

    def _fetch(self) -> str:
        try:
            ua = UserAgent()
            headers = {"User-Agent": ua.random}
            r = httpx.get(self.url, headers=headers)
            r.raise_for_status()
        except httpx.HTTPError:
            print(r.response)
            print(r.text)
            print("could not fetch page")
            return None
        return r.text

    def _fetch_from_cache(self) -> str:
        with open(self.filepath) as f:
            html = f.read()
        return html

    def _save_to_cache(self, html):
        with open(self.filepath, "w") as f:
            f.write(html)
