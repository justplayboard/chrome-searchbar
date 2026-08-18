"""
Autocomplete Manager
"""


from search.providers.history import HistoryProvider
from search.providers.google import GoogleProvider
from search.providers.github import GitHubProvider
from search.providers.youtube import YouTubeProvider
from search.providers.naver import NaverProvider


class AutoCompleteManager:

    def __init__(self, history, settings):

        self.history = history
        self.settings = settings

        self.providers = {

            "history": HistoryProvider(self.history),

            "google": GoogleProvider(),

            "github": GitHubProvider(),

            "youtube": YouTubeProvider(),

            "naver": NaverProvider(),
        }

    def complete(self, text):

        if not text:

            return []

        text = text.lower()

        result = []

        result.extend(
            self.providers.get("history").suggest(text)
        )

        engine = self.settings.get_search_engine()

        provider = self.providers.get(engine)

        if provider:

            result.extend(
                provider.suggest(text)
            )

        result.sort(
            key=lambda x: x.priority
        )

        return self._remove_duplicates(result)

    def _remove_duplicates(self, suggestions):

        result = []

        seen = set()

        for item in suggestions:

            key = item.text.lower()

            if key in seen:

                continue

            seen.add(key)

            result.append(item)

        return result