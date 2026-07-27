"""
chrome.py

Chrome launcher and Google search handler
"""

import subprocess


def open_url(
    browser: str,
    url: str,
):

    command = [
        "cmd",
        "/c",
        "start",
        browser,
        url,
    ]

    try:

        subprocess.Popen(
            command,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

    except Exception as exc:

        raise RuntimeError(
            f"Failed to launch {browser}"
        ) from exc
    
    return