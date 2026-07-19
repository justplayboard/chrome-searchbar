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

from config import (
    APP_NAME,
    ICON_PATH,
)


class TrayManager(QObject):
    """
    Manage Windows system tray icon.
    """


    def __init__(self, search_bar):
        super().__init__()

        self.search_bar = search_bar

        self.tray = None

        self.create_tray()



    def create_tray(self):
        """
        Create tray icon and menu.
        """


        self.tray = QSystemTrayIcon()


        # Icon
        if ICON_PATH.exists():

            self.tray.setIcon(
                QIcon(str(ICON_PATH))
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
            self.show_search_bar
        )


        hide_action = QAction(
            "검색창 숨기기",
            self
        )

        hide_action.triggered.connect(
            self.hide_search_bar
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



    def show_search_bar(self):
        """
        Show search window.
        """

        self.search_bar.show()

        self.search_bar.activateWindow()

        self.search_bar.input.setFocus()



    def hide_search_bar(self):
        """
        Hide search window.
        """

        self.search_bar.hide()



    def tray_clicked(self, reason):
        """
        Handle tray icon click.
        """

        if reason == QSystemTrayIcon.ActivationReason.Trigger:

            self.show_search_bar()



    def quit_app(self):
        """
        Quit application completely.
        """

        self.tray.hide()

        QApplication.quit()