"""
searchbar.py

Main floating search bar UI
Chrome Desktop Search Bar
"""

from PyQt5.QtCore import (
    Qt,
    QPoint,
    QStringListModel,
    QThread,
    pyqtSignal,
    QTimer,
    QSize,
)
from PyQt5.QtGui import (
    QFont,
    QCursor,
    QIcon,
)
from PyQt5.QtWidgets import (
    QWidget,
    QFrame,
    QLineEdit,
    QLabel,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
    QCompleter,
)

from config.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TOP_MARGIN,
    WINDOW_RADIUS,
    SHADOW_BLUR,
    SHADOW_OFFSET_X,
    SHADOW_OFFSET_Y,
    SHADOW_ALPHA,
    SEARCH_ICON,
    ICON_CHROME_PATH,
    ICON_BRAVE_PATH,
)

from ui.style import apply_search_style

from ui.suggestion_popup import SuggestionPopup

from ui.search_line_edit import SearchLineEdit

from core.services import ServiceContainer

from search.suggestion_worker import SuggestionWorker


class SearchBar(QWidget):
    """
    Floating desktop search bar.
    """


    requestSuggestions = pyqtSignal(
        int,
        str
    )


    def __init__(
        self,
        services: ServiceContainer,
    ):
        super().__init__()

        self.setObjectName("SearchBar")

        self.drag_position = None
        self.request_id = 0
        self._settings_open = False

        self.settings = services.settings
        self.search_service = services.search_service
        self.autocomplete = services.autocomplete
        self.logger = services.logger

        self.settings.opacityChanged.connect(
            self.set_window_opacity
        )

        self.init_window()
        self.init_ui()
        self.init_history()
        self.init_completion()
        self.init_suggestion_worker()
        self.apply_shadow()
        self.restore_position()

        apply_search_style(self)

        self.show()
        self.activateWindow()
        self.input.setFocus()


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
            # Qt.WindowType.WindowStaysOnTopHint
            # |
            Qt.WindowType.Tool
        )


        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )


        self.setFixedSize(
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )

        self.set_window_opacity(self.settings.get_opacity())


    # ------------------------------------------------------
    # UI
    # ------------------------------------------------------

    def init_ui(self):
        """
        Create widgets.
        """


        # Container widget
        self.container = QFrame(self)

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

        self.change_icon()

        self.settings.browserChanged.connect(
            self.change_icon
        )

        self.icon.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        # Input box
        self.input = SearchLineEdit()

        self.change_placeholder()

        self.input.returnPressed.connect(
            self.search
        )

        self.settings.searchEngineChanged.connect(
            self.change_placeholder
        )

        self.input.installEventFilter(self)


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


        # self.input.setCompleter(
        #     self.completer
        # )


        self.update_history()

        self.settings.historyChanged.connect(
            self.update_history
        )



    def update_history(self):

        history = self.search_service.history_list()


        self.history_model.setStringList(
            history
        )



    def init_completion(self):

        self.popup = SuggestionPopup()

        self.popup.set_callback(
            self.select_completion
        )

        self.input.searchTextEdited.connect(
            self.update_completion
        )

        self.input.compositionStarted.connect(
            self.on_composition_started
        )

        self.input.compositionFinished.connect(
            self.on_composition_finished
        )



    def select_completion(self, text):

        self.input.setText(text)

        self.input.setCursorPosition(
            len(text)
        )

        self.popup.hide()

        self.input.setFocus()



    def update_completion(self, text):

        if self.input.is_composing:

            return

        if not text:

            self.popup.hide()

            return

        self.popup.move(
            self.x(),
            self.y() + self.height()
        )

        self.popup.resize(
            self.width(),
            360
        )

        self.debounce_timer.start()

        self.input.setFocus()



    def on_composition_started(self):

        self.popup.hide()

        self.debounce_timer.stop()



    def on_composition_finished(self):

        self.debounce_timer.start()



    def init_suggestion_worker(self):

        self.thread = QThread()

        self.worker = SuggestionWorker(
            self.autocomplete
        )

        self.worker.moveToThread(
            self.thread
        )

        self.thread.start()

        self.requestSuggestions.connect(
            self.worker.request
        )

        self.worker.suggestionsReady.connect(
            self.onSuggestionsReady
        )

        self.worker.errorOccurred.connect(
            lambda msg: self.logger.error(msg)
        )

        self.debounce_timer = QTimer(self)

        self.debounce_timer.setSingleShot(True)

        self.debounce_timer.setInterval(300)

        self.debounce_timer.timeout.connect(
            self.send_suggestion_request
        )



    def send_suggestion_request(self):

        keyword = self.input.text().strip()

        if not keyword:

            return

        self.request_id += 1

        self.requestSuggestions.emit(
            self.request_id,
            keyword
        )



    def onSuggestionsReady(
        self,
        request_id,
        items
    ):

        if request_id != self.request_id:

            return

        self.popup.update_items(items)



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
            None
        )



    # ------------------------------------------------------
    # Icon
    # ------------------------------------------------------

    def change_icon(self):

        browser = self.settings.get_browser()

        ico = SEARCH_ICON

        if browser == "chrome":

            ico = ICON_CHROME_PATH

        elif browser == "brave":

            ico = ICON_BRAVE_PATH

        if ico == SEARCH_ICON:

            self.icon.setText(
                ico
            )

        else:

            ico = str(ico)

            icon = QIcon(ico)

            pixmap = icon.pixmap(QSize(32, 32))

            self.icon.setPixmap(pixmap)



    # ------------------------------------------------------
    # Placeholder
    # ------------------------------------------------------

    def change_placeholder(self):

        self.input.setPlaceholderText(
            self.settings.get_search_engine() + " 검색"
        )



    # ------------------------------------------------------
    # Search
    # ------------------------------------------------------

    def search(self):
        """
        Execute Google search.
        """

        keyword = self.input.text()

        if not self.search_service.search(keyword):
            return

        self.update_history()

        self.input.clear()

        # Hide after search
        self.popup.hide()
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



    # ------------------------------------------------------
    # Opacity
    # ------------------------------------------------------

    def set_window_opacity(
        self,
        opacity: float,
    ):
        
        self.setWindowOpacity(opacity)



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

        self.thread.quit()

        self.thread.wait()

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

            if self.popup.isVisible():

                pos = self.mapToGlobal(
                    QPoint(0, self.height())
                )

                self.popup.move(pos)


            event.accept()



    def mouseReleaseEvent(self, event):

        self.drag_position = None

        self.save_position()



    # def keyPressEvent(self, event):

    #     if self.popup.isVisible():

    #         if event.key() == Qt.Key_Down:

    #             self.popup.move_selection(
    #                 1
    #             )

    #             return
            
    #         if event.key() == Qt.Key_Up:

    #             self.popup.move_selection(
    #                 -1
    #             )

    #             return
            
    #         if event.key() == Qt.Key_Return:

    #             text = self.popup.selected_text()

    #             if text:

    #                 self.select_completion(
    #                     text
    #                 )

    #             return
            
    #         if event.key() == Qt.Key_Escape:

    #             self.popup.hide()

    #             return
            
    #     super().keyPressEvent(event)



    def eventFilter(self, obj, event):

        if obj == self.input:

            if event.type() == event.KeyPress:

                key = event.key()

                if self.popup.isVisible():

                    if key == Qt.Key_Down:

                        self.popup.move_selection(
                            1
                        )

                        return True
                    
                    if key == Qt.Key_Up:

                        self.popup.move_selection(
                            -1
                        )

                        return True
                    
                    if key == Qt.Key_Return:

                        text = self.popup.selected_text()

                        if text:

                            self.select_completion(
                                text
                            )

                        return True
                    
                    if key == Qt.Key_Escape:

                        self.popup.hide()

                        return True
                    
        return super().eventFilter(
            obj,
            event
        )