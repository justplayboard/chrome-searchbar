"""
History suggestion provider
"""


from .base import SuggestionProvider

from search.suggestion import Suggestion



class HistoryProvider(SuggestionProvider):


    def __init__(self, history):

        self.history = history



    def suggest(self, keyword):

        if not keyword:

            return []


        keyword = keyword.lower()


        result = []


        for item in self.history.get_history():


            if item.lower().startswith(keyword):

                result.append(
                    Suggestion(
                        text=item,
                        provider="history",
                        icon="🕘",
                        description="최근 검색",
                        priority=0,
                        category="history",
                    )
                )


        return result