"""
ui/hotkey_edit.py

Hotkey capture widget
Compatible with Windows RegisterHotKey
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit


# Qt Key → 문자열
SPECIAL_KEYS = {
    Qt.Key_Space: "Space",
    Qt.Key_Tab: "Tab",
    Qt.Key_Backtab: "Tab",

    Qt.Key_Return: "Enter",
    Qt.Key_Enter: "Enter",

    Qt.Key_Escape: "Esc",

    Qt.Key_Backspace: "Backspace",

    Qt.Key_Delete: "Delete",

    Qt.Key_Insert: "Insert",

    Qt.Key_Home: "Home",

    Qt.Key_End: "End",

    Qt.Key_PageUp: "PageUp",

    Qt.Key_PageDown: "PageDown",

    Qt.Key_Left: "Left",

    Qt.Key_Right: "Right",

    Qt.Key_Up: "Up",

    Qt.Key_Down: "Down",
}


class HotkeyEdit(QLineEdit):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setPlaceholderText("Press shortcut")

        self.setReadOnly(True)

        self._hotkey = ""

    # -------------------------------------------------

    def keyPressEvent(self, event):

        modifiers = []

        mod = event.modifiers()

        if mod & Qt.ControlModifier:
            modifiers.append("Ctrl")

        if mod & Qt.AltModifier:
            modifiers.append("Alt")

        if mod & Qt.ShiftModifier:
            modifiers.append("Shift")

        if mod & Qt.MetaModifier:
            modifiers.append("Win")

        key = event.key()

        # Modifier만 눌렀을 경우 무시
        if key in (
            Qt.Key_Control,
            Qt.Key_Shift,
            Qt.Key_Alt,
            Qt.Key_Meta,
        ):
            return

        key_name = self.key_to_string(key)

        if key_name is None:
            return

        sequence = modifiers + [key_name]

        self._hotkey = "+".join(sequence)

        self.setText(self._hotkey)

    # -------------------------------------------------

    def key_to_string(self, key):

        # 특수키
        if key in SPECIAL_KEYS:
            return SPECIAL_KEYS[key]

        # A~Z
        if Qt.Key_A <= key <= Qt.Key_Z:
            return chr(key)

        # 0~9
        if Qt.Key_0 <= key <= Qt.Key_9:
            return chr(key)

        # F1~F24
        if Qt.Key_F1 <= key <= Qt.Key_F24:
            return f"F{key - Qt.Key_F1 + 1}"

        return None

    # -------------------------------------------------

    def hotkey(self):

        return self._hotkey

    # -------------------------------------------------

    def setHotkey(self, hotkey):

        self._hotkey = hotkey

        self.setText(hotkey)

    # -------------------------------------------------

    def clear(self):

        self._hotkey = ""

        super().clear()