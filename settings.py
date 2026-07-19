"""
settings.py

User preference manager
Chrome Search Bar
"""

from PyQt5.QtCore import QSettings

from config import (
    APP_NAME,
)


class SettingsManager:
    """
    Manage application settings.
    """


    def __init__(self):

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
            "ctrl+space"
        )


    def set_hotkey(self, hotkey):
        """
        Save global hotkey.
        """

        self.settings.setValue(
            "hotkey",
            hotkey
        )


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
        opacity
    ):
        """
        Save window opacity.
        """

        self.settings.setValue(
            "window/opacity",
            opacity
        )



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
        enabled
    ):
        """
        Save startup option.
        """

        self.settings.setValue(
            "startup/enabled",
            enabled
        )



    # ==================================================
    # Search Engine
    # ==================================================

    def get_search_engine(self):
        """
        Get current search engine.
        """

        return self.settings.value(
            "search/engine",
            "Google"
        )



    def set_search_engine(
        self,
        engine
    ):
        """
        Save search engine.
        """

        self.settings.setValue(
            "search/engine",
            engine
        )



    # ==================================================
    # Generic
    # ==================================================

    def remove_all(self):
        """
        Clear all settings.
        """

        self.settings.clear()