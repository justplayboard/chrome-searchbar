"""
tray.py

System tray manager
Chrome Search Bar
"""

from PyQt5.QtWidgets import (
    QSystemTrayIcon,
    QMenu,
    QApplication,
    QAction,
)

from PyQt5.QtGui import (
    QIcon,
)

from PyQt5.QtCore import QObject

from config.constants import (
    APP_NAME,
    ICON_PATH,
    ICON_CHROME_PATH,
)

from ui.searchbar import SearchBar

from ui.settings_dialog import SettingsDialog

from core.services import ServiceContainer


class TrayManager(QObject):
    """
    Manage Windows system tray icon.
    """


    def __init__(
        self,
        search_bar: SearchBar,
        services: ServiceContainer,
    ):
        super().__init__()

        self.search_bar = search_bar
        self.services = services
        self.settings = services.settings
        self.startup = services.startup

        self.tray = None

        self.create_tray()



    def create_tray(self):
        """
        Create tray icon and menu.
        """


        self.tray = QSystemTrayIcon()


        # Icon
        if ICON_CHROME_PATH.exists():

            self.tray.setIcon(
                QIcon(str(ICON_CHROME_PATH))
            )

        else:

            # 아이콘 파일이 없을 경우
            # 기본 아이콘 사용

            self.tray.setIcon(
                QApplication.style()
                .standardIcon(
                    QApplication.style()
                    .StandardPixmap.SP_ComputerIcon
                )
            )


        self.tray.setToolTip(
            APP_NAME
        )


        # Context menu
        menu = QMenu()


        show_action = QAction(
            "검색창 열기",
            self
        )

        show_action.triggered.connect(
            self.search_bar.show_search_bar
        )


        hide_action = QAction(
            "검색창 숨기기",
            self
        )

        hide_action.triggered.connect(
            self.hide_search_bar
        )


        self.startup_action = QAction(
            "Windows 시작 시 실행",
            self.tray
        )

        self.startup_action.setCheckable(True)

        self.startup_action.setChecked(
            self.startup.is_enabled()
        )

        self.startup_action.triggered.connect(
            self.toggle_startup
        )


        self.settings_action = QAction(
            "설정",
            self
        )

        self.settings_action.triggered.connect(
            self.show_settings
        )


        quit_action = QAction(
            "종료",
            self
        )

        quit_action.triggered.connect(
            self.quit_app
        )


        menu.addAction(
            show_action
        )

        menu.addAction(
            hide_action
        )

        # menu.addAction(
        #     self.startup_action
        # )

        menu.addAction(
            self.settings_action
        )

        menu.addSeparator()

        menu.addAction(
            quit_action
        )


        self.tray.setContextMenu(
            menu
        )


        # Click event
        self.tray.activated.connect(
            self.tray_clicked
        )


    def show(self):
        """
        Display tray icon.
        """

        self.tray.show()



    def show_settings(self):

        if self.search_bar._settings_open:

            return

        self.search_bar._settings_open = True

        dialog = SettingsDialog(self.services, self.search_bar)

        dialog.finished.connect(
            self.close_settings
        )

        self.search_bar.show()

        dialog.exec()



    def close_settings(self):

        self.search_bar._settings_open = False



    def show_search_bar(self):
        """
        Show search window.
        """

        self.search_bar.show()

        self.search_bar.raise_()

        self.search_bar.activateWindow()

        self.search_bar.input.setFocus()



    def hide_search_bar(self):
        """
        Hide search window.
        """

        if self.search_bar._settings_open:

            return

        self.search_bar.popup.hide()
        self.search_bar.hide()



    def toggle_startup(self):

        enabled = self.startup_action.isChecked()

        self.settings.set_startup_enabled(enabled)

        if enabled:

            self.startup.enable()

        else:

            self.startup.disable()



    def tray_clicked(self, reason):
        """
        Handle tray icon click.
        """

        if reason == QSystemTrayIcon.ActivationReason.Trigger:

            self.search_bar.show_search_bar()



    def quit_app(self):
        """
        Quit application completely.
        """

        app = QApplication.instance()

        if app is not None:

            self.tray.hide()

            app.quit()