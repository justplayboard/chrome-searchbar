"""
services/search_service.py

Search service

검색과 관련된 비즈니스 로직을 담당한다.
"""

from core.history import HistoryManager

from core.settings import SettingsManager

from services.chrome import open_url

from search.registry import SearchEngineRegistry


class SearchService:
    """
    Search service.
    """

    def __init__(
        self,
        history: HistoryManager,
        settings: SettingsManager,
        registry: SearchEngineRegistry,
        logger,
    ):

        self.history = history
        self.settings = settings
        self.logger = logger

        self.current_engine = self.settings.get_search_engine()

        self.settings.searchEngineChanged.connect(
            self.change_engine
        )

        self.registry = registry


    # ==================================================
    # Public
    # ==================================================

    def search(
        self,
        keyword: str,
    ) -> bool:
        """
        Execute search.

        Returns
        -------
        bool
            True if search executed.
        """

        keyword = keyword.strip()

        if not keyword:

            self.logger.warning(
                "Search cancelled: empty keyword"
            )

            return False
        
        self.logger.info(
            "Search: %s",
            keyword
        )

        #
        # Save history
        #
        self.history.add(keyword)

        #
        # Open Chrome
        #
        try:

            engine = self.registry.get(
                self.current_engine
            )

            url = engine.build_url(keyword)

            open_url(url)

            self.logger.info(
                "Chrome launched successfully: %s",
                self.current_engine
            )

            return True

        except Exception:

            self.logger.exception(
                "Failed to execute search"
            )

            return False


    def history_list(self):

        return self.history.get_history()


    def clear_history(self):

        self.history.clear()


    def change_engine(
        self,
        engine: str,
    ):
        
        self.current_engine = engine