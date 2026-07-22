"""
Suggestion popup
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem

from ui.style import SUGGESTION_STYLE

from ui.suggestion_item import SuggestionItem


class SuggestionPopup(QListWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.parent_bar = parent

        self.callback = None

        self.hide()

        self.setWindowFlags(
            Qt.Tool |
            Qt.FramelessWindowHint |
            Qt.NoDropShadowWindowHint
        )

        self.setFocusPolicy(
            Qt.NoFocus
        )

        self.setStyleSheet(
            SUGGESTION_STYLE
        )

        self.itemClicked.connect(
            self.item_selected
        )

    # -----------------------------

    def set_callback(self, callback):

        self.callback = callback

    # -----------------------------

    def update_items(
        self,
        suggestions
    ):

        self.clear()

        if not suggestions:

            self.hide()

            return

        for suggestion in suggestions:

            item = QListWidgetItem(self)

            widget = SuggestionItem(suggestion)

            item.setSizeHint(
                widget.sizeHint()
            )

            self.addItem(item)

            self.setItemWidget(
                item,
                widget
            )

        self.setCurrentRow(0)

        self.show()

    # -----------------------------

    def item_selected(self, item):

        row = self.row(item)

        widget = self.itemWidget(item)

        if widget and self.callback:

            self.callback(
                widget.suggestion.text
            )

        self.hide()

    # -----------------------------

    def move_selection(self, direction):

        row = self.currentRow()

        count = self.count()

        if count == 0:

            return
        
        new_row = row + direction

        if new_row < 0:

            new_row = count - 1

        elif new_row >= count:

            new_row = 0

        self.setCurrentRow(
            new_row
        )

    # -----------------------------

    def selected_text(self):

        item = self.currentItem()

        if not item:

            return None

        widget = self.itemWidget(item)

        if widget:

            return widget.suggestion.text
        
        return None