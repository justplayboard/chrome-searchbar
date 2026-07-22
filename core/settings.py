"""
settings.py

User preference manager
Chrome Search Bar
"""

from PyQt5.QtCore import QSettings, QObject, pyqtSignal

from config.constants import (
    APP_NAME,
)


class SettingsManager(QObject):
    """
    Manage application settings.
    """


    hotkeyChanged = pyqtSignal(str)
    searchEngineChanged = pyqtSignal(str)
    opacityChanged = pyqtSignal(float)
    startupChanged = pyqtSignal(bool)
    historyChanged = pyqtSignal(bool)


    def __init__(self):

        super().__init__()

        self.settings = QSettings(
            APP_NAME,
            APP_NAME
        )


    # ==================================================
    # Hotkey
    # ==================================================

    def get_hotkey(self):
        """
        Get global hotkey.
        """

        return self.settings.value(
            "hotkey",
            "Ctrl+Alt+Shift+Space"
        )


    def set_hotkey(
        self,
        hotkey: str,
    ):
        """
        Save global hotkey.
        """

        hotkey = hotkey.strip()

        current = self.get_hotkey()

        if current == hotkey:

            return

        self.settings.setValue(
            "hotkey",
            hotkey
        )

        self.hotkeyChanged.emit(hotkey)


    # ==================================================
    # Window
    # ==================================================

    def get_window_position(self):
        """
        Load window position.

        Returns:
            tuple or None
        """

        x = self.settings.value(
            "window/x",
            None
        )

        y = self.settings.value(
            "window/y",
            None
        )


        if x is None or y is None:

            return None


        return (
            int(x),
            int(y)
        )



    def set_window_position(
        self,
        x,
        y
    ):
        """
        Save window position.
        """

        self.settings.setValue(
            "window/x",
            x
        )

        self.settings.setValue(
            "window/y",
            y
        )



    # ==================================================
    # Window Appearance
    # ==================================================

    def get_opacity(self):
        """
        Get window opacity.
        """

        return float(
            self.settings.value(
                "window/opacity",
                0.98
            )
        )



    def set_opacity(
        self,
        opacity: float,
    ):
        """
        Save window opacity.
        """

        opacity = max(0.3, min(1.0, opacity))

        self.settings.setValue(
            "window/opacity",
            opacity
        )

        self.opacityChanged.emit(opacity)



    # ==================================================
    # Startup
    # ==================================================

    def get_startup_enabled(self):
        """
        Check Windows startup option.
        """

        value = self.settings.value(
            "startup/enabled",
            False
        )


        return value in (
            True,
            "true",
            "True",
            1,
            "1"
        )



    def set_startup_enabled(
        self,
        enabled: bool,
    ):
        """
        Save startup option.
        """

        current = self.get_startup_enabled()

        if current == enabled:

            return

        self.settings.setValue(
            "startup/enabled",
            enabled
        )

        self.startupChanged.emit(enabled)



    # ==================================================
    # Search Engine
    # ==================================================

    def get_search_engine(self):
        """
        Get current search engine.
        """

        return self.settings.value(
            "search/engine",
            "google"
        )



    def set_search_engine(
        self,
        engine: str,
    ):
        """
        Save search engine.
        """

        current = self.get_search_engine()

        if current == engine:

            return

        self.settings.setValue(
            "search/engine",
            engine
        )

        self.searchEngineChanged.emit(engine)



    # ==================================================
    # Generic
    # ==================================================

    def remove_all(self):
        """
        Clear all settings.
        """

        self.settings.clear()