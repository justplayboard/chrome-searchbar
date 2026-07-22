"""
chrome.py

Chrome launcher and Google search handler
"""

import subprocess


def open_url(url: str):

    command = [
        "cmd",
        "/c",
        "start",
        "chrome",
        url,
    ]

    try:

        subprocess.Popen(command)

    except Exception as exc:

        raise RuntimeError(
            "Failed to launch Chrome"
        ) from exc
    
    return