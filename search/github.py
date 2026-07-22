from urllib.parse import quote

from search.base import SearchEngine


class GitHubEngine(SearchEngine):

    name = "github"

    display_name = "GitHub"

    def build_url(
        self,
        keyword: str,
    ) -> str:

        return (
            "https://github.com/search?q="
            + quote(keyword)
        )