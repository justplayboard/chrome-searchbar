"""
Base class for search engines.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class SearchEngine(ABC):

    name = ""

    display_name = ""

    @abstractmethod
    def build_url(
        self,
        keyword: str,
    ) -> str:
        pass