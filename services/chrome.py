"""
chrome.py

Chrome launcher and Google search handler
"""

import os
import subprocess
import urllib.parse
import webbrowser

from config.constants import (
    DEFAULT_CHROME_PATHS,
    GOOGLE_SEARCH_URL,
)


def find_chrome():
    """
    Find installed Google Chrome executable.

    Returns:
        str | None:
            Chrome executable path
    """

    for path in DEFAULT_CHROME_PATHS:

        if path and os.path.exists(path):
            return path

    return None


def create_search_url(keyword):
    """
    Create Google search URL.

    Args:
        keyword (str):
            Search keyword

    Returns:
        str:
            Encoded Google search URL
    """

    keyword = keyword.strip()

    if not keyword:
        return None

    encoded_keyword = urllib.parse.quote(keyword)

    return GOOGLE_SEARCH_URL.format(encoded_keyword)


def open_chrome_search(keyword):
    """
    Open Google search using Chrome.

    Args:
        keyword (str):
            Search keyword
    """

    url = create_search_url(keyword)

    if not url:
        return


    chrome_path = find_chrome()


    # Chrome found
    if chrome_path:

        subprocess.Popen(
            [
                chrome_path,
                url,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return


    # Chrome not found
    # fallback to default browser

    webbrowser.open(url)