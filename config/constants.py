"""
constants.py

Application configuration
Chrome Search Bar
"""

from pathlib import Path
import os
import sys


# ==========================================================
# Application
# ==========================================================

APP_NAME = "Chrome Search Bar"
APP_VERSION = "1.0.0"


# ==========================================================
# Window
# ==========================================================

WINDOW_WIDTH = 620
WINDOW_HEIGHT = 52

WINDOW_RADIUS = 18

WINDOW_OPACITY = 0.98

WINDOW_TOP_MARGIN = 60


# ==========================================================
# Search
# ==========================================================

GOOGLE_SEARCH_URL = "https://www.google.com/search?q={}"


# ==========================================================
# Colors
# ==========================================================

BACKGROUND_COLOR = "#FFFFFF"

TEXT_COLOR = "#202124"

PLACEHOLDER_COLOR = "#80868B"

BORDER_COLOR = "#DADCE0"

FOCUS_BORDER_COLOR = "#4285F4"

SHADOW_COLOR = "#000000"


# ==========================================================
# Shadow
# ==========================================================

SHADOW_BLUR = 25

SHADOW_OFFSET_X = 0

SHADOW_OFFSET_Y = 3

SHADOW_ALPHA = 55


# ==========================================================
# Font
# ==========================================================

FONT_FAMILY = "Segoe UI"

FONT_SIZE = 12


# ==========================================================
# Search Icon
# ==========================================================

SEARCH_ICON = "🔍"


# ==========================================================
# Browser
# ==========================================================

BROWSER_LIST = [

    "chrome",

    "brave",
]


# ==========================================================
# Chrome
# ==========================================================

DEFAULT_CHROME_PATHS = [

    r"C:\Program Files\Google\Chrome\Application\chrome.exe",

    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",

    os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        r"Google\Chrome\Application\chrome.exe",
    ),
]


# ==========================================================
# Resource Directory
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[1]

RESOURCE_DIR = BASE_DIR / "resources"

ICON_PATH = RESOURCE_DIR / "icon.ico"

ICON_CHROME_PATH = RESOURCE_DIR / "icon-chrome.ico"

ICON_BRAVE_PATH = RESOURCE_DIR / "icon-brave.ico"


# ==========================================================
# Resource Path
# ==========================================================

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)