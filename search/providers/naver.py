"""
NAVER suggestion provider
"""


import requests

from .base import SuggestionProvider

from search.suggestion import Suggestion



class NaverProvider(SuggestionProvider):

    URL = (
        "https://ac.search.naver.com/"
        "nx/ac"
    )


    def suggest(self, keyword):

        if not keyword:

            return []

        # 다음 단계에서 API 연결

        try:

            params = {
                "q": keyword,
                "st": "100",
                "r_format": "json",
            }

            headers = {
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/131.0.0.0 Safari/537.36"
                )
            }

            response = requests.get(
                self.URL,
                params=params,
                headers=headers,
                timeout=2,
            )

            response.raise_for_status()

            data = response.json()

        except Exception:

            return []


        result = []

        for item in data["items"][0]:

            if not item:

                continue

            text = item[0]

            result.append(
                Suggestion(
                    text=text,
                    provider="naver",
                    icon="🗨️",
                    description="NAVER 추천",
                    priority=10,
                    category="search",
                )
            )

        return result