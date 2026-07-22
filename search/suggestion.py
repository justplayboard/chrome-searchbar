"""
search/suggestion.py
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Suggestion:
    """
    자동완성 항목
    """

    text: str

    provider: str

    icon: str = ""

    description: str = ""

    priority: int = 100

    category: str = ""