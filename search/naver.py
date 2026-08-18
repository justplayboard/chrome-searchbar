from urllib.parse import quote

from search.base import SearchEngine


class NaverEngine(SearchEngine):

    name = "naver"

    display_name = "NAVER"

    def build_url(
        self,
        keyword: str,
    ) -> str:

        return (
            "https://search.naver.com/search.naver?query="
            + quote(keyword)
        )