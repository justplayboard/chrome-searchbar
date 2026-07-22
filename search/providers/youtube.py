"""
YouTube suggestion provider
"""


import requests

from .base import SuggestionProvider

from search.suggestion import Suggestion



class YouTubeProvider(SuggestionProvider):

    URL = (
        "https://suggestqueries.google.com/"
        "complete/search"
    )


    def suggest(self, keyword):

        if not keyword:

            return []

        try:

            params = {
                "client": "firefox",
                "ds": "yt",
                "q": keyword,
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

        for text in data[1]:

            result.append(
                Suggestion(
                    text=text,
                    provider="youtube",
                    icon="▶️",
                    description="YouTube 추천",
                    priority=10,
                    category="search",
                )
            )

        return result