"""
hotkey.py

Global hotkey manager
Chrome Search Bar
"""

from __future__ import annotations

import string

import ctypes
from ctypes import wintypes

from PyQt5.QtCore import QObject, QAbstractNativeEventFilter

from PyQt5.QtWidgets import QApplication

from ui.searchbar import SearchBar

from core.services import ServiceContainer



# --------------------------------------------------
# Windows API
# --------------------------------------------------

user32 = ctypes.windll.user32

WM_HOTKEY = 0x0312

MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
MOD_WIN = 0x0008

VK_SPACE = 0x20

HOTKEY_ID = 1

MODIFIERS = {
    "CTRL": MOD_CONTROL,
    "CONTROL": MOD_CONTROL,
    "ALT": MOD_ALT,
    "SHIFT": MOD_SHIFT,
    "WIN": MOD_WIN,
}

VK_CODES = {
    "SPACE": 0x20,
    "TAB": 0x09,
    "ENTER": 0x0D,
    "ESC": 0x1B,
    "ESCAPE": 0x1B,

    "UP": 0x26,
    "DOWN": 0x28,
    "LEFT": 0x25,
    "RIGHT": 0x27,

    "HOME": 0x24,
    "END": 0x23,

    "PAGEUP": 0x21,
    "PAGEDOWN": 0x22,

    "INSERT": 0x2D,
    "DELETE": 0x2E,
}


# --------------------------------------------------
# Native Event Filter
# --------------------------------------------------

class HotkeyEventFilter(
    QAbstractNativeEventFilter
):
    """
    Receives WM_HOTKEY messages.
    """

    def __init__(self, callback):

        super().__init__()

        self.callback = callback

    def nativeEventFilter(
        self,
        eventType,
        message,
    ):

        if eventType != b"windows_generic_MSG":

            return False, 0

        msg = wintypes.MSG.from_address(
            int(message)
        )

        if msg.message == WM_HOTKEY:

            self.callback()

            return True, 0

        return False, 0


# --------------------------------------------------
# Manager
# --------------------------------------------------

class HotkeyManager(QObject):
    """
    Manage global keyboard shortcuts.
    """


    def __init__(
        self,
        search_bar: SearchBar,
        services: ServiceContainer,
        logger,
    ):
        super().__init__()

        self._init_keys()

        self.search_bar = search_bar
        self.settings = services.settings
        self.logger = logger

        self.settings.hotkeyChanged.connect(
            self.reload_hotkey
        )

        self.filter = HotkeyEventFilter(
            self.on_hotkey
        )

        QApplication.instance().installNativeEventFilter(
            self.filter
        )

        self.register(self.settings.get_hotkey())



    def _init_keys(self):

        for c in string.ascii_uppercase:

            VK_CODES[c] = ord(c)

        for i in range(10):

            VK_CODES[str(i)] = ord(str(i))

        for i in range(1, 25):

            VK_CODES[f"F{i}"] = 0x70 + i - 1



    def parse_hotkey(self, hotkey: str):

        modifier = 0
        vk = None

        for part in hotkey.upper().split("+"):

            part = part.strip()

            if part in MODIFIERS:

                modifier |= MODIFIERS[part]

            elif part in VK_CODES:

                vk = VK_CODES[part]

            else:

                raise ValueError(
                    f"Unknown hotkey: {part}"
                )

        if vk is None:

            raise ValueError(
                "No virtual key found."
            )

        return modifier, vk



    def register(self, hotkey):
        """
        Register global hotkey.
        """

        modifier, vk = self.parse_hotkey(hotkey)

        ok = user32.RegisterHotKey(
            None,
            HOTKEY_ID,
            modifier,
            vk,
        )

        if not ok:

            error = ctypes.get_last_error()

            raise RuntimeError(
                f"RegisterHotKey failed ({error})"
            )

        self.logger.info(
            "Global hotkey registered: %s",
            hotkey
        )



    def unregister(self):
        """
        Remove registered hotkeys.
        """

        user32.UnregisterHotKey(
            None,
            HOTKEY_ID,
        )

        self.logger.info(
            "Global hotkey removed"
        )



    def shutdown(self):

        user32.UnregisterHotKey(
            None,
            HOTKEY_ID,
        )

        QApplication.instance().removeNativeEventFilter(
            self.filter
        )



    def reload_hotkey(
        self,
        hotkey: str,
    ):
        
        try:
        
            self.unregister()

        except Exception:

            pass

        self.register(hotkey)



    def on_hotkey(self):

        if self.search_bar.isVisible():

            self.search_bar.hide_search_bar()

        else:

            self.search_bar.show_search_bar()