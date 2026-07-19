"""
main.py

Chrome Desktop Search Bar
Application Entry Point
"""

import sys

from PyQt5.QtWidgets import QApplication

from searchbar import SearchBar
from tray import TrayManager
from hotkey import HotkeyManager


def main():
    """Application entry point."""

    app = QApplication(sys.argv)

    # 프로그램 이름
    app.setApplicationName("Chrome Search Bar")
    app.setApplicationDisplayName("Chrome Search Bar")

    # 메인 검색창 생성
    search_bar = SearchBar()

    tray = TrayManager(
        search_bar
    )
    tray.show()

    hotkey = HotkeyManager(
        search_bar
    )

    sys.exit(app.exec())


if __name__ == "__main__":
    main()