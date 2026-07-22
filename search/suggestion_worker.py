"""
search/suggestion_worker.py

Autocomplete worker thread
"""

import traceback

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class SuggestionWorker(QObject):

    suggestionsReady = pyqtSignal(
        int,
        list
    )

    errorOccurred = pyqtSignal(str)


    def __init__(self, manager):

        super().__init__()

        self.manager = manager


    @pyqtSlot(int, str)
    def request(
        self,
        request_id,
        keyword
    ):

        try:

            result = self.manager.complete(keyword)

            self.suggestionsReady.emit(
                request_id,
                result
            )

        except Exception:

            self.errorOccurred.emit(
                traceback.format_exc()
            )