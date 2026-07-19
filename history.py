"""
history.py

Search history manager
Chrome Search Bar
"""

from PyQt5.QtCore import QSettings

from config import APP_NAME


class HistoryManager:
    """
    Manage search history.
    """


    MAX_HISTORY_COUNT = 50


    def __init__(self):

        self.settings = QSettings(
            APP_NAME,
            APP_NAME
        )

        self.key = "search/history"



    def get_history(self):
        """
        Load search history.

        Returns:
            list[str]
        """

        history = self.settings.value(
            self.key,
            []
        )


        if history is None:

            return []


        # QSettings may return string
        # when only one item exists
        if isinstance(
            history,
            str
        ):

            return [history]


        return list(history)



    def add(self, keyword):
        """
        Add search keyword.

        Args:
            keyword(str)
        """

        keyword = keyword.strip()


        if not keyword:

            return


        history = self.get_history()


        # Remove duplicate
        if keyword in history:

            history.remove(keyword)


        # Add newest first
        history.insert(
            0,
            keyword
        )


        # Limit size
        history = history[
            :self.MAX_HISTORY_COUNT
        ]


        self.settings.setValue(
            self.key,
            history
        )



    def remove(self, keyword):
        """
        Remove one keyword.
        """

        history = self.get_history()


        if keyword in history:

            history.remove(
                keyword
            )


        self.settings.setValue(
            self.key,
            history
        )



    def clear(self):
        """
        Delete all search history.
        """

        self.settings.remove(
            self.key
        )



    def count(self):
        """
        Return history count.
        """

        return len(
            self.get_history()
        )