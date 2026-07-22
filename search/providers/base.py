"""
Autocomplete provider base
"""


from abc import ABC, abstractmethod

from search.suggestion import Suggestion


class SuggestionProvider(ABC):


    @abstractmethod
    def suggest(self, keyword: str) -> list[Suggestion]:
        """
        Return suggestion list
        """

        pass