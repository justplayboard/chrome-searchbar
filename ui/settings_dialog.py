"""
ui/settings_dialog.py

Application Settings Dialog
"""

from __future__ import annotations

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSlider,
    QVBoxLayout,
)

from ui.hotkey_edit import HotkeyEdit


class SettingsDialog(QDialog):

    def __init__(
        self,
        services,
        parent=None,
    ):

        super().__init__(parent)

        self.services = services

        self.setWindowTitle("Settings")

        self.setMinimumWidth(420)

        self.build_ui()

        self.load_settings()

    # -------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(self)

        form = QFormLayout()

        #
        # Search Engine
        #
        self.engine_combo = QComboBox()

        self.engine_combo.addItems(
            self.services.registry.names()
        )

        form.addRow(
            "Search Engine",
            self.engine_combo,
        )

        #
        # Hotkey
        #
        self.hotkey_edit = HotkeyEdit()

        form.addRow(
            "Hotkey",
            self.hotkey_edit,
        )

        #
        # Opacity
        #
        self.opacity_slider = QSlider(
            Qt.Orientation.Horizontal
        )

        self.opacity_slider.setRange(
            30,
            100,
        )

        self.opacity_label = QLabel()

        opacity_layout = QHBoxLayout()

        opacity_layout.addWidget(
            self.opacity_slider
        )

        opacity_layout.addWidget(
            self.opacity_label
        )

        form.addRow(
            "Opacity",
            opacity_layout,
        )

        #
        # Startup
        #
        self.startup_check = QCheckBox(
            "Run at Windows startup"
        )

        form.addRow(
            "",
            self.startup_check,
        )

        layout.addLayout(form)

        #
        # History
        #
        self.clear_history_button = QPushButton(
            "Clear Search History"
        )

        layout.addWidget(
            self.clear_history_button
        )

        #
        # OK / Cancel
        #
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            |
            QDialogButtonBox.StandardButton.Cancel
        )

        layout.addWidget(
            self.buttons
        )

        #
        # Signal
        #
        self.opacity_slider.valueChanged.connect(
            self.update_opacity_label
        )

        self.buttons.accepted.connect(
            self.accept
        )

        self.buttons.rejected.connect(
            self.reject
        )

        self.clear_history_button.clicked.connect(
            self.clear_history
        )

    # -------------------------------------------------

    def load_settings(self):

        settings = self.services.settings

        self.engine_combo.setCurrentText(
            settings.get_search_engine()
        )

        self.hotkey_edit.setHotkey(
            settings.get_hotkey()
        )

        opacity = int(
            settings.get_opacity() * 100
        )

        self.opacity_slider.setValue(opacity)

        self.startup_check.setChecked(
            settings.get_startup_enabled()
        )

        self.update_opacity_label(opacity)

    # -------------------------------------------------

    def update_opacity_label(
        self,
        value,
    ):

        self.opacity_label.setText(
            f"{value}%"
        )

        self.services.settings.opacityChanged.emit(value / 100)

    # -------------------------------------------------

    def clear_history(self):

        self.services.history.clear()

        self.services.settings.historyChanged.emit(True)

    # -------------------------------------------------

    def accept(self):

        settings = self.services.settings

        settings.set_search_engine(
            self.engine_combo.currentText()
        )

        settings.set_hotkey(
            self.hotkey_edit.hotkey()
        )

        settings.set_opacity(
            self.opacity_slider.value() / 100
        )

        settings.set_startup_enabled(
            self.startup_check.isChecked()
        )

        super().accept()

    # -------------------------------------------------

    def reject(self):

        settings = self.services.settings

        settings.set_opacity(
            settings.get_opacity()
        )

        super().reject()