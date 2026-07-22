"""
main.py

Chrome Desktop Search Bar
Application Entry Point
"""

import sys

from PyQt5.QtWidgets import QApplication

from app import ApplicationController


def main():
    """Application entry point."""

    qt_app = QApplication(sys.argv)

    # 프로그램 이름
    qt_app.setApplicationName("Chrome Search Bar")
    qt_app.setApplicationDisplayName("Chrome Search Bar")

    controller = ApplicationController(qt_app)

    controller.start()

    exit_code = qt_app.exec()

    controller.shutdown()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()