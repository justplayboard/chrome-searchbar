from urllib.parse import quote

from search.base import SearchEngine


class GoogleEngine(SearchEngine):

    name = "google"

    display_name = "Google"

    def build_url(
        self,
        keyword: str,
    ) -> str:

        return (
            "https://www.google.com/search?q="
            + quote(keyword)
        )