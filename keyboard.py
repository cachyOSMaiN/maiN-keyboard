"""Virtual keyboard widget with PyQt6."""

import importlib

from PyQt6.QtWidgets import (
    QWidget, QPushButton, QSizePolicy, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont
from evdev import ecodes

from input_emitter import InputEmitter

AVAILABLE_LAYOUTS = ['de', 'uk', 'us']

LAYOUT_NAMES = {
    'de': 'Deutsch (DE)',
    'uk': 'English UK',
    'us': 'English US',
}


class KeyButton(QPushButton):
    """A single key button on the virtual keyboard."""

    def __init__(self, normal: str, shifted: str, keycode: int, modifier_keys: set, wide_keys: dict, parent=None):
        super().__init__(normal, parent)
        self.normal_label = normal
        self.shifted_label = shifted
        self.keycode = keycode
        self.is_modifier = keycode in modifier_keys

        base_width = 50
        width_multiplier = wide_keys.get(keycode, 1.0)
        self.key_width = int(base_width * width_multiplier)

        self.setMinimumSize(QSize(self.key_width, 50))
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        font = QFont()
        font.setPointSize(14)
        self.setFont(font)

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def update_label(self, shift_active: bool):
        """Update button label based on shift state."""
        if not self.is_modifier:
            label = self.shifted_label if shift_active else self.normal_label
            # Qt interprets single '&' as a mnemonic; escape it to '&&' to display literal text.
            self.setText(label.replace("&", "&&"))


class KeyboardWidget(QWidget):
    """The main virtual keyboard widget."""

    layout_changed = pyqtSignal(str)

    BASE_STYLE = """
        KeyButton {
            background-color: #3a3a3a;
            color: #ffffff;
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 5px;
        }
        KeyButton:hover {
            background-color: #4a4a4a;
        }
        KeyButton:pressed {
            background-color: #2a2a2a;
        }
        KeyButton[active="true"] {
            background-color: #5a7aa5;
            border-color: #7a9ac5;
        }
        QWidget {
            background-color: #2d2d2d;
        }
    """

    BASE_FONT_SIZE = 14

    def __init__(self, layout='de', parent=None):
        super().__init__(parent)

        self.emitter = InputEmitter()
        self.shift_active = False
        self.caps_active = False
        self.buttons: list[KeyButton] = []
        self.current_layout = layout
        self._current_scale = 1.0

        # Main layout holds the keyboard container
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)

        # Container widget for keyboard keys
        self._container = None

        self._load_layout(layout)
        self._build_keyboard()
        self.setStyleSheet(self.BASE_STYLE)

    def _load_layout(self, name: str):
        """Load layout data from the specified layout module."""
        module = importlib.import_module(f'layouts.{name}')
        self.LAYOUT = module.LAYOUT
        self.MODIFIER_KEYS = module.MODIFIER_KEYS
        self.WIDE_KEYS = module.WIDE_KEYS

    def set_layout(self, name: str):
        """Change to a different keyboard layout."""
        if name == self.current_layout:
            return

        self.current_layout = name
        self._load_layout(name)
        self._rebuild_keyboard()
        self.layout_changed.emit(name)

    def _rebuild_keyboard(self):
        """Rebuild the keyboard with the current layout."""
        # Remove old container
        if self._container:
            self._main_layout.removeWidget(self._container)
            self._container.deleteLater()
            self._container = None

        self.buttons.clear()
        self.shift_active = False
        self.caps_active = False

        # Build new keyboard
        self._build_keyboard()
        self.set_scale(self._current_scale)

    def _build_keyboard(self):
        """Build the keyboard UI in a container widget."""
        self._container = QWidget()
        container_layout = QVBoxLayout(self._container)
        container_layout.setSpacing(4)
        container_layout.setContentsMargins(8, 8, 8, 8)

        for row_data in self.LAYOUT:
            row_layout = QHBoxLayout()
            row_layout.setSpacing(4)

            for normal, shifted, keycode in row_data:
                btn = KeyButton(normal, shifted, keycode, self.MODIFIER_KEYS, self.WIDE_KEYS)
                btn.clicked.connect(lambda checked, k=keycode, b=btn: self._on_key_clicked(k, b))
                row_layout.addWidget(btn)
                self.buttons.append(btn)

            container_layout.addLayout(row_layout)

        self._main_layout.addWidget(self._container)

    def set_scale(self, factor: float):
        """Scale the font size of all buttons."""
        self._current_scale = factor
        new_size = int(self.BASE_FONT_SIZE * factor)
        for btn in self.buttons:
            font = btn.font()
            font.setPointSize(new_size)
            btn.setFont(font)

    def _on_key_clicked(self, keycode: int, button: KeyButton):
        """Handle key button click."""
        if keycode in (ecodes.KEY_LEFTSHIFT, ecodes.KEY_RIGHTSHIFT):
            self.shift_active = not self.shift_active
            self._update_modifier_state(button, self.shift_active)
            self._update_all_labels()
            return

        if keycode == ecodes.KEY_CAPSLOCK:
            self.caps_active = not self.caps_active
            self._update_modifier_state(button, self.caps_active)
            self._update_all_labels()
            return

        if keycode in (ecodes.KEY_LEFTCTRL, ecodes.KEY_LEFTALT, ecodes.KEY_RIGHTALT):
            is_active = self.emitter.toggle_modifier(keycode)
            self._update_modifier_state(button, is_active)
            return

        # Regular key
        if button.normal_label.isalpha() and len(button.normal_label) == 1:
            apply_shift = self.shift_active != self.caps_active
        else:
            apply_shift = self.shift_active

        self.emitter.send_key(keycode, with_shift=apply_shift)

        if self.shift_active:
            self.shift_active = False
            self._update_shift_buttons(False)
            self._update_all_labels()

        self.emitter.release_all_modifiers()
        self._update_ctrl_alt_buttons()

    def _update_modifier_state(self, button: KeyButton, active: bool):
        """Update visual state of a modifier button."""
        button.setProperty('active', active)
        button.style().unpolish(button)
        button.style().polish(button)

    def _update_shift_buttons(self, active: bool):
        """Update all shift button states."""
        for btn in self.buttons:
            if btn.keycode in (ecodes.KEY_LEFTSHIFT, ecodes.KEY_RIGHTSHIFT):
                self._update_modifier_state(btn, active)

    def _update_ctrl_alt_buttons(self):
        """Update ctrl/alt button states based on emitter state."""
        for btn in self.buttons:
            if btn.keycode in (ecodes.KEY_LEFTCTRL, ecodes.KEY_LEFTALT, ecodes.KEY_RIGHTALT):
                is_active = self.emitter.is_modifier_active(btn.keycode)
                self._update_modifier_state(btn, is_active)

    def _update_all_labels(self):
        """Update all button labels based on current shift/caps state."""
        for btn in self.buttons:
            if btn.normal_label.isalpha() and len(btn.normal_label) == 1:
                show_shifted = self.shift_active != self.caps_active
            else:
                show_shifted = self.shift_active
            btn.update_label(show_shifted)

    def move_window_to_monitor(self, direction: str):
        """Move the active window to another monitor using Win+Shift+Arrow."""
        arrow_key = ecodes.KEY_LEFT if direction == 'left' else ecodes.KEY_RIGHT

        self.emitter.device.write(ecodes.EV_KEY, ecodes.KEY_LEFTMETA, 1)
        self.emitter.device.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 1)
        self.emitter.device.syn()

        self.emitter.device.write(ecodes.EV_KEY, arrow_key, 1)
        self.emitter.device.syn()
        self.emitter.device.write(ecodes.EV_KEY, arrow_key, 0)
        self.emitter.device.syn()

        self.emitter.device.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 0)
        self.emitter.device.write(ecodes.EV_KEY, ecodes.KEY_LEFTMETA, 0)
        self.emitter.device.syn()

    def closeEvent(self, event):
        """Clean up when widget is closed."""
        self.emitter.close()
        super().closeEvent(event)
