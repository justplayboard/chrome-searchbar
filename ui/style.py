"""
style.py

Qt Style Sheet definitions
Chrome Search Bar
"""

from config.constants import (
    BACKGROUND_COLOR,
    TEXT_COLOR,
    PLACEHOLDER_COLOR,
    BORDER_COLOR,
    FOCUS_BORDER_COLOR,
    FONT_FAMILY,
    FONT_SIZE,
)


SEARCH_BAR_STYLE = f"""
/* Main window */
#SearchBar {{
    background-color: transparent;
    font-family: "{FONT_FAMILY}";
    font-size: {FONT_SIZE}px;
}}


/* Search container */
#SearchContainer {{
    background-color: {BACKGROUND_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: 18px;
}}


/* Search icon */
#SearchIcon {{
    color: {TEXT_COLOR};
    font-size: 20px;
    padding-left: 14px;
    padding-right: 8px;
    background: transparent;
}}


/* Search input */
QLineEdit {{
    background-color: transparent;
    border: none;
    color: {TEXT_COLOR};
    font-size: 15px;
    padding-left: 5px;
    padding-right: 15px;
}}


/* Placeholder text */
QLineEdit::placeholder {{
    color: {PLACEHOLDER_COLOR};
}}


/* Focus effect */
#SearchContainer:focus-within {{
    border: 2px solid {FOCUS_BORDER_COLOR};
}}
"""


SUGGESTION_STYLE = """

QListWidget {

    background-color: white;

    border-radius: 10px;

    border: 1px solid #dddddd;

}


QListWidget::item:selected {

    background-color: #e8f0fe;

}


QLabel {

    background: transparent;

}

"""


def apply_search_style(widget):
    """
    Apply application style to widget.
    """

    widget.setStyleSheet(SEARCH_BAR_STYLE)