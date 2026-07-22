"""
app.py

Application Controller

모든 핵심 객체의 생성과 생명주기를 관리한다.
"""

from PyQt5.QtWidgets import QApplication

from core.settings import SettingsManager
from core.history import HistoryManager
from core.startup import StartupManager
from core.logger import LoggingManager
from core.services import ServiceContainer
from search.registry import SearchEngineRegistry
from search.autocomplete import AutoCompleteManager

from ui.searchbar import SearchBar
from ui.tray import TrayManager

from services.hotkey import HotkeyManager
from services.search_service import SearchService


class ApplicationController:
    """
    Central application controller.
    """

    def __init__(self, qt_app: QApplication):

        self.qt_app = qt_app

        # Core Services
        self.settings = None
        self.history = None
        self.startup = None

        # UI
        self.search_bar = None
        self.tray = None

        # System
        self.hotkey = None

        self._initialize()


    # ==================================================
    # Initialize
    # ==================================================

    def _initialize(self):

        self._create_core()

        self._create_ui()

        self._create_services()


    # ==================================================
    # Core
    # ==================================================

    def _create_core(self):

        self.logger = LoggingManager().logger

        self.settings = SettingsManager()

        self.history = HistoryManager(
            self.logger
        )

        self.startup = StartupManager(
            self.settings,
            self.logger
        )

        self.registry = SearchEngineRegistry()

        self.autocomplete = AutoCompleteManager(
            self.history,
            self.settings
        )

        self.services = ServiceContainer(
            settings=self.settings,
            history=self.history,
            startup=self.startup,
            registry=self.registry,
            autocomplete=self.autocomplete,
            logger=self.logger
        )

        self.services.search_service = SearchService(
            history=self.services.history,
            settings=self.services.settings,
            registry=self.services.registry,
            logger=self.services.logger
        )


    # ==================================================
    # UI
    # ==================================================

    def _create_ui(self):

        #
        # 현재 SearchBar는
        # 아직 SettingsManager와 HistoryManager를
        # 생성자에서 받지 않으므로
        # 기존 방식으로 생성한다.
        #
        # 다음 단계에서 변경한다.
        #

        self.search_bar = SearchBar(
            services=self.services
        )

        self.tray = TrayManager(
            search_bar=self.search_bar,
            services=self.services
        )


    # ==================================================
    # Services
    # ==================================================

    def _create_services(self):

        self.hotkey = HotkeyManager(
            search_bar=self.search_bar,
            services=self.services,
            logger=self.logger
        )


    # ==================================================
    # Public
    # ==================================================

    def start(self):
        """
        Start application.
        """

        self.tray.show()

        self.logger.info("Application started")


    def shutdown(self):
        """
        Graceful shutdown.
        """

        #
        # 이후 단계에서
        #
        # logger flush
        # hotkey unregister
        # settings save
        #
        # 등을 추가한다.
        #

        self.logger.info("Application shutdown")

        try:

            if self.hotkey:

                shutdown = getattr(
                    self.hotkey,
                    "shutdown",
                    None
                )

                if callable(shutdown):

                    shutdown()

        finally:

            self.qt_app.quit()