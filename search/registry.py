"""
search/registry.py

Search Engine Registry
"""

from __future__ import annotations

from search.google import GoogleEngine
from search.github import GitHubEngine
from search.youtube import YouTubeEngine
from search.naver import NaverEngine
# from search.chatgpt import ChatGPTEngine
# from search.perplexity import PerplexityEngine


class SearchEngineRegistry:

    def __init__(self):

        self._engines = {}

        self.register(GoogleEngine())
        self.register(GitHubEngine())
        self.register(YouTubeEngine())
        self.register(NaverEngine())
        # self.register(ChatGPTEngine())
        # self.register(PerplexityEngine())

    # ------------------------------------------

    def register(self, engine):

        self._engines[engine.name] = engine

    # ------------------------------------------

    def get(self, name):

        return self._engines[name]

    # ------------------------------------------

    def names(self):

        return list(self._engines.keys())
    
    # ------------------------------------------

    def items(self):

        return [
            (engine.name, engine.display_name)
            for engine in self._engines.values()
        ]

    # ------------------------------------------

    def all(self):

        return dict(self._engines)