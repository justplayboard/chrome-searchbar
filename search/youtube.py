from urllib.parse import quote

from search.base import SearchEngine


class YouTubeEngine(SearchEngine):

    name = "youtube"

    display_name = "Youtube"

    def build_url(
        self,
        keyword: str,
    ) -> str:

        return (
            "https://www.youtube.com/results?search_query="
            + quote(keyword)
        )