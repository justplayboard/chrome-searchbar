"""
searchbar.py

Main floating search bar UI
Chrome Desktop Search Bar
"""

from PyQt5.QtCore import (
    Qt,
    QPoint,
    QStringListModel,
)
from PyQt5.QtGui import (
    QFont,
    QCursor,
)
from PyQt5.QtWidgets import (
    QWidget,
    QLineEdit,
    QLabel,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
    QCompleter,
)

from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TOP_MARGIN,
    WINDOW_RADIUS,
    SHADOW_BLUR,
    SHADOW_OFFSET_X,
    SHADOW_OFFSET_Y,
    SHADOW_ALPHA,
    SEARCH_ICON,
)

from style import apply_search_style

from chrome import open_chrome_search

from history import HistoryManager

from settings import SettingsManager


class SearchBar(QWidget):
    """
    Floating desktop search bar.
    """


    def __init__(self):
        super().__init__()

        self.drag_position = None

        self.settings = SettingsManager()
        self.history = HistoryManager()

        self.init_window()
        self.init_ui()
        self.init_history()
        self.apply_shadow()
        self.restore_position()

        apply_search_style(self)


    # ------------------------------------------------------
    # Window configuration
    # ------------------------------------------------------

    def init_window(self):
        """
        Configure frameless always-on-top window.
        """

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            |
            Qt.WindowType.WindowStaysOnTopHint
            |
            Qt.WindowType.Tool
        )


        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )


        self.setFixedSize(
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )


    # ------------------------------------------------------
    # UI
    # ------------------------------------------------------

    def init_ui(self):
        """
        Create widgets.
        """


        # Container widget
        self.container = QWidget(self)

        self.container.setObjectName(
            "SearchContainer"
        )


        self.container.setGeometry(
            0,
            0,
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )


        # Search icon
        self.icon = QLabel()

        self.icon.setObjectName(
            "SearchIcon"
        )

        self.icon.setText(
            SEARCH_ICON
        )


        self.icon.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        # Input box
        self.input = QLineEdit()

        self.input.setPlaceholderText(
            "Google 검색"
        )


        self.input.returnPressed.connect(
            self.search
        )


        # Layout
        layout = QHBoxLayout(
            self.container
        )


        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )


        layout.setSpacing(
            0
        )


        layout.addWidget(
            self.icon
        )


        layout.addWidget(
            self.input
        )


        self.input.setFocus()



    # =====================================================
    # History / Auto completion
    # =====================================================

    def init_history(self):

        self.history_model = QStringListModel()


        self.completer = QCompleter(
            self.history_model,
            self
        )


        self.completer.setCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )


        self.input.setCompleter(
            self.completer
        )


        self.update_history()



    def update_history(self):

        history = self.history.get_history()


        self.history_model.setStringList(
            history
        )



    # ------------------------------------------------------
    # Shadow
    # ------------------------------------------------------

    def apply_shadow(self):
        """
        Add floating shadow effect.
        """

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(
            SHADOW_BLUR
        )

        shadow.setOffset(
            SHADOW_OFFSET_X,
            SHADOW_OFFSET_Y
        )


        color = Qt.GlobalColor.black

        shadow.setColor(
            color
        )


        self.container.setGraphicsEffect(
            shadow
        )



    # ------------------------------------------------------
    # Search
    # ------------------------------------------------------

    def search(self):
        """
        Execute Google search.
        """

        keyword = self.input.text().strip()

        if not keyword:
            return

        # save history
        self.history.add(keyword)

        self.update_history()

        # Open Chrome
        open_chrome_search(
            keyword
        )

        self.input.clear()

        # Hide after search
        self.hide()



    # ------------------------------------------------------
    # Position
    # ------------------------------------------------------

    def restore_position(self):

        position = self.settings.get_window_position()

        if position:
            self.move(
                position[0],
                position[1]
            )

        else:
            self.move_to_top_center()

    def move_to_top_center(self):
        """
        Move window to top center of screen.
        """

        screen = self.screen()

        if not screen:
            return


        geometry = screen.availableGeometry()


        x = (
            geometry.center().x()
            -
            self.width() // 2
        )


        y = (
            geometry.top()
            +
            WINDOW_TOP_MARGIN
        )


        self.move(
            x,
            y
        )



    # =====================================================
    # Save position
    # =====================================================

    def save_position(self):

        self.settings.set_window_position(
            self.x(),
            self.y()
        )



    def closeEvent(self, event):

        self.save_position()

        event.accept()



    # ------------------------------------------------------
    # Drag movement
    # ------------------------------------------------------

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.drag_position = (
                event.globalPos()
                -
                self.frameGeometry().topLeft()
            )


            event.accept()



    def mouseMoveEvent(self, event):

        if (
            event.buttons()
            &
            Qt.MouseButton.LeftButton
            and
            self.drag_position
        ):

            self.move(
                event.globalPos()
                -
                self.drag_position
            )


            event.accept()



    def mouseReleaseEvent(self, event):

        self.drag_position = None

        self.save_position()