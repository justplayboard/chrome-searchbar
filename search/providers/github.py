"""
GitHub suggestion provider
"""


import requests

from .base import SuggestionProvider

from search.suggestion import Suggestion



class GitHubProvider(SuggestionProvider):

    URL = (
        "https://api.github.com/"
        "search/repositories"
    )


    def suggest(self, keyword):

        if not keyword:

            return []

        try:

            params = {
                "q": keyword,
                "per_page": 5,
            }

            response = requests.get(
                self.URL,
                params=params,
                timeout=2,
            )

            response.raise_for_status()

            data = response.json()

        except Exception:

            return []

        result = []

        for repo in data.get("items", []):

            result.append(
                Suggestion(
                    text=repo["full_name"],
                    provider="github",
                    icon="💻",
                    description="GitHub 저장소",
                    priority=10,
                    category="search",
                )
            )

        return result