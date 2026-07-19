"""
hotkey.py

Global hotkey manager
Chrome Search Bar
"""

import keyboard

from PyQt5.QtCore import QObject, pyqtSignal


class HotkeyManager(QObject):
    """
    Manage global keyboard shortcuts.
    """


    # Main Thread로 전달할 신호
    toggle_signal = pyqtSignal()

    def __init__(
        self,
        search_bar,
        hotkey="ctrl+space"
    ):
        super().__init__()

        self.search_bar = search_bar

        self.hotkey = hotkey

        # Signal 연결
        self.toggle_signal.connect(
            self.toggle_search_bar
        )

        self.register()



    def register(self):
        """
        Register global hotkey.
        """

        keyboard.add_hotkey(
            self.hotkey,
            self.emit_toggle
        )


    def emit_toggle(self):
        """
        Keyboard thread에서 실행됨.
        Signal만 발생시킨다.
        """

        self.toggle_signal.emit()


    def toggle_search_bar(self):
        """
        Show or hide search bar.
        """

        if self.search_bar.isVisible():

            self.hide_search_bar()

        else:

            self.show_search_bar()



    def show_search_bar(self):
        """
        Show search window.
        """

        self.search_bar.show()

        self.search_bar.activateWindow()

        self.search_bar.raise_()

        self.search_bar.input.setFocus()



    def hide_search_bar(self):
        """
        Hide search window.
        """

        self.search_bar.hide()



    def unregister(self):
        """
        Remove registered hotkeys.
        """

        keyboard.unhook_all()