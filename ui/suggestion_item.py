"""
ui/suggestion_item.py

Custom suggestion widget
"""


from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)

from PyQt5.QtCore import Qt


EMOJI_MAP = {

    "history": "🕘",

    "google": "🌐",

    "github": "💻",

    "youtube": "▶️",

    "naver": "🗨️",

}


class SuggestionItem(QWidget):


    def __init__(
        self,
        suggestion,
        parent=None,
    ):

        super().__init__(parent)


        self.suggestion = suggestion


        self.build_ui()



    def build_ui(self):


        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            10,
            5,
            10,
            5,
        )


        icon = EMOJI_MAP.get(
            self.suggestion.provider,
            "🔍"
        )


        self.title = QLabel(
            f"{icon}  {self.suggestion.text}"
        )


        self.description = QLabel(
            self.suggestion.description
        )


        self.description.setStyleSheet(
            """
            color: gray;
            font-size: 11px;
            """
        )


        layout.addWidget(
            self.title
        )

        layout.addWidget(
            self.description
        )