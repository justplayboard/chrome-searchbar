"""
startup.py

Windows startup manager
Chrome Search Bar
"""

import sys
import os
import winreg

from config import APP_NAME


# Registry location
STARTUP_KEY = (
    r"Software\Microsoft\Windows\CurrentVersion\Run"
)


class StartupManager:
    """
    Manage Windows startup registration.
    """


    def __init__(self):
        self.app_name = APP_NAME



    def get_executable_path(self):
        """
        Get current application executable path.

        When running from Python:
            use python script path

        When packaged:
            use exe path
        """

        if getattr(
            sys,
            "frozen",
            False
        ):

            return sys.executable


        return (
            f'"{sys.executable}" '
            f'"{os.path.abspath(sys.argv[0])}"'
        )



    def enable(self):
        """
        Enable startup execution.
        """

        path = self.get_executable_path()


        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            STARTUP_KEY,
            0,
            winreg.KEY_SET_VALUE
        ) as key:

            winreg.SetValueEx(
                key,
                self.app_name,
                0,
                winreg.REG_SZ,
                path
            )



    def disable(self):
        """
        Remove startup registration.
        """

        try:

            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                STARTUP_KEY,
                0,
                winreg.KEY_SET_VALUE
            ) as key:

                winreg.DeleteValue(
                    key,
                    self.app_name
                )


        except FileNotFoundError:

            pass



    def is_enabled(self):
        """
        Check startup status.
        """

        try:

            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                STARTUP_KEY,
                0,
                winreg.KEY_READ
            ) as key:


                winreg.QueryValueEx(
                    key,
                    self.app_name
                )


            return True


        except FileNotFoundError:

            return False