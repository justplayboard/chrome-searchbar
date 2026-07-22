"""
core/services.py
"""

from dataclasses import dataclass
from typing import Optional

from core.settings import SettingsManager
from core.history import HistoryManager
from core.startup import StartupManager
from search.registry import SearchEngineRegistry
from search.autocomplete import AutoCompleteManager
from services.search_service import SearchService


@dataclass(slots=True)
class ServiceContainer:
    """
    모든 공유 서비스 보관
    """

    settings: SettingsManager

    history: HistoryManager

    startup: StartupManager

    registry: SearchEngineRegistry

    autocomplete: AutoCompleteManager

    logger: object

    search_service: Optional[SearchService] = None