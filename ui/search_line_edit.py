"""
ui/search_line_edit.py

Custom QLineEdit with proper IME composition support.
"""

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit


class SearchLineEdit(QLineEdit):

    #
    # Signals
    #
    compositionStarted = pyqtSignal()

    compositionFinished = pyqtSignal()

    searchTextEdited = pyqtSignal(str)

    def __init__(self, parent=None):

        super().__init__(parent)

        self._composing = False

        #
        # 기존 textEdited는 내부에서만 받는다.
        #
        self.textEdited.connect(
            self._on_text_edited
        )

    # ---------------------------------------------------------

    @property
    def is_composing(self):

        return self._composing

    # ---------------------------------------------------------

    def _on_text_edited(self, text):

        #
        # IME 조합 중이면 무시
        #
        if self._composing:
            return

        self.searchTextEdited.emit(text)

    # ---------------------------------------------------------

    def inputMethodEvent(self, event):

        preedit = event.preeditString()

        #
        # 조합 시작
        #
        if preedit and not self._composing:

            self._composing = True

            self.compositionStarted.emit()

        #
        # 조합 종료
        #
        if self._composing and not event.preeditString():

            self._composing = False

            # self.compositionFinished.emit()

            #
            # 여기서 현재 text()를 다시 전달
            #
            self.searchTextEdited.emit(
                self.text()
            )

        super().inputMethodEvent(event)