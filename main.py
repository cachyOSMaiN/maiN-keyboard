#!/usr/bin/env python3
"""
Virtual On-Screen Keyboard for KDE/Wayland

Runs under XWayland for better focus handling.
"""

import sys
import os
import json
import socket

# Force XWayland mode for better focus handling
os.environ['QT_QPA_PLATFORM'] = 'xcb'

CONFIG_FILE = os.path.expanduser('~/.config/osk/settings.json')

from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout,
    QVBoxLayout, QLabel, QPushButton,
    QSystemTrayIcon, QMenu
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication, QIcon, QAction, QActionGroup

from keyboard import KeyboardWidget, AVAILABLE_LAYOUTS, LAYOUT_NAMES


def load_config():
    """Load settings from config file."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_config(config):
    """Save settings to config file."""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)


class TitleBar(QWidget):
    """Custom title bar with drag support and close button."""

    STYLE = """
        TitleBar {
            background-color: #131315;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }
        QLabel {
            color: #8e8e93;
            font-size: 12px;
            padding-left: 8px;
        }
        QPushButton {
            background-color: transparent;
            color: #8e8e93;
            border: none;
            font-size: 16px;
            padding: 4px 12px;
        }
        QPushButton:hover {
            background-color: #3a3a3c;
            color: white;
        }
        QPushButton#close_btn:hover {
            background-color: #c42b1c;
            border-top-right-radius: 8px;
        }
        QPushButton#layout_btn {
            font-size: 12px;
            font-weight: bold;
            padding: 4px 8px;
        }
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.window_parent = parent
        self._drag_pos = None

        self.setFixedHeight(32)
        self.setStyleSheet(self.STYLE)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Title label
        self.title_label = QLabel("MaiN_Keyboard")
        self.title_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        layout.addWidget(self.title_label)

        # Spacer
        spacer = QWidget()
        spacer.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        spacer.setSizePolicy(spacer.sizePolicy().Policy.Expanding, spacer.sizePolicy().Policy.Preferred)
        layout.addWidget(spacer)

        # Monitor switch buttons
        self.mon_left_btn = QPushButton("<-")
        self.mon_left_btn.setFixedSize(40, 32)
        self.mon_left_btn.setStyleSheet("margin-right: -6px;")
        self.mon_left_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.mon_left_btn.clicked.connect(lambda: self._on_move_monitor('left'))
        layout.addWidget(self.mon_left_btn)

        # Window move icon
        self.window_icon = QLabel("󰆍")
        self.window_icon.setFixedWidth(24)
        self.window_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.window_icon.setStyleSheet("color: #8e8e93; font-size: 14px; padding: 0;")
        layout.addWidget(self.window_icon)

        self.mon_right_btn = QPushButton("->")
        self.mon_right_btn.setFixedSize(40, 32)
        self.mon_right_btn.setStyleSheet("margin-left: 0px;")
        self.mon_right_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.mon_right_btn.clicked.connect(lambda: self._on_move_monitor('right'))
        layout.addWidget(self.mon_right_btn)

        # Bring icon to front (above both buttons)
        self.mon_left_btn.stackUnder(self.window_icon)
        self.mon_right_btn.stackUnder(self.window_icon)

        # Separator
        sep = QWidget()
        sep.setFixedWidth(10)
        layout.addWidget(sep)

        # Layout button
        self.layout_btn = QPushButton("DE")
        self.layout_btn.setObjectName("layout_btn")
        self.layout_btn.setFixedSize(40, 32)
        self.layout_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.layout_btn.setToolTip("Tastaturlayout wechseln")
        self.layout_btn.clicked.connect(self._on_layout_cycle)
        layout.addWidget(self.layout_btn)

        # Separator
        sep2 = QWidget()
        sep2.setFixedWidth(10)
        layout.addWidget(sep2)

        # Scale buttons
        self.scale_s_btn = QPushButton("S")
        self.scale_s_btn.setFixedSize(40, 32)
        self.scale_s_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.scale_s_btn.clicked.connect(lambda: self._on_scale(1.0))
        layout.addWidget(self.scale_s_btn)

        self.scale_m_btn = QPushButton("M")
        self.scale_m_btn.setFixedSize(40, 32)
        self.scale_m_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.scale_m_btn.clicked.connect(lambda: self._on_scale(1.2))
        layout.addWidget(self.scale_m_btn)

        self.scale_b_btn = QPushButton("B")
        self.scale_b_btn.setFixedSize(40, 32)
        self.scale_b_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.scale_b_btn.clicked.connect(lambda: self._on_scale(1.6))
        layout.addWidget(self.scale_b_btn)

        # Close button
        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("close_btn")
        self.close_btn.setFixedSize(46, 32)
        self.close_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.close_btn.clicked.connect(self._on_close)
        layout.addWidget(self.close_btn)

    def update_layout_button(self, layout_name: str):
        """Update the layout button text."""
        self.layout_btn.setText(layout_name.upper())

    def _on_layout_cycle(self):
        """Cycle through available layouts."""
        if self.window_parent:
            self.window_parent.cycle_layout()

    def _on_close(self):
        self.window_parent.hide()

    def _on_scale(self, factor):
        if self.window_parent:
            self.window_parent.set_scale(factor)

    def _on_move_monitor(self, direction):
        if self.window_parent:
            self.window_parent.keyboard.move_window_to_monitor(direction)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.window_parent.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_pos:
            self.window_parent.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None


class VirtualKeyboard(QWidget):
    """Main window for the virtual keyboard."""

    def __init__(self):
        super().__init__()

        # Window flags for OSK behavior under X11/XWayland
        self.setWindowFlags(
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.X11BypassWindowManagerHint
        )

        # Prevent focus stealing
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WidgetAttribute.WA_X11DoNotAcceptFocus)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Load saved settings
        config = load_config()
        self._current_scale = config.get('scale', 1.0)
        self._current_layout = config.get('layout', 'de')
        self._current_opacity = config.get('opacity', 1.0)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Title bar
        self.title_bar = TitleBar(self)
        layout.addWidget(self.title_bar)

        # Keyboard with saved layout
        self.keyboard = KeyboardWidget(layout=self._current_layout)
        self.keyboard.layout_changed.connect(self._on_layout_changed)
        layout.addWidget(self.keyboard)

        # Update title bar button
        self.title_bar.update_layout_button(self._current_layout)

        # Styling
        self.setStyleSheet("background-color: #131315; border-radius: 8px;")

        # Base dimensions
        self._base_width = 900
        self._base_height = 312

        # Position at bottom and apply scale
        self._position_at_bottom()
        self.keyboard.set_scale(self._current_scale)
        self.setWindowOpacity(self._current_opacity)

        # Tray menu actions (will be set by main())
        self.layout_actions = {}
        self.opacity_actions = {}

    def _on_layout_changed(self, layout_name: str):
        """Handle layout change from keyboard widget."""
        self._current_layout = layout_name
        self.title_bar.update_layout_button(layout_name)

        # Update tray menu checkmarks
        for name, action in self.layout_actions.items():
            action.setChecked(name == layout_name)

    def cycle_layout(self):
        """Cycle to the next layout."""
        current_idx = AVAILABLE_LAYOUTS.index(self._current_layout)
        next_idx = (current_idx + 1) % len(AVAILABLE_LAYOUTS)
        new_layout = AVAILABLE_LAYOUTS[next_idx]
        self.keyboard.set_layout(new_layout)

    def set_layout(self, name: str):
        """Set a specific layout."""
        self.keyboard.set_layout(name)

    def _position_at_bottom(self):
        """Position the keyboard at the bottom center of the screen."""
        screen = QGuiApplication.primaryScreen()
        if screen:
            geo = screen.availableGeometry()
            width = min(int(self._base_width * self._current_scale), geo.width() - 40)
            height = int(self._base_height * self._current_scale)
            x = geo.x() + (geo.width() - width) // 2
            y = geo.y() + geo.height() - height - 58
            self.setGeometry(x, y, width, height)

    def set_scale(self, factor):
        """Scale the keyboard to the given factor."""
        self._current_scale = factor
        self._position_at_bottom()
        self.keyboard.set_scale(factor)

    def set_opacity(self, opacity: float):
        """Set the window opacity and save to config."""
        self._current_opacity = opacity
        self.setWindowOpacity(opacity)
        # Update tray menu checkmarks
        for value, action in self.opacity_actions.items():
            action.setChecked(value == opacity)
        # Save setting
        config = load_config()
        config['opacity'] = opacity
        save_config(config)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            QApplication.quit()
        else:
            super().keyPressEvent(event)

    def hideEvent(self, event):
        """Save settings when hiding."""
        config = load_config()
        config['scale'] = self._current_scale
        config['layout'] = self._current_layout
        save_config(config)
        super().hideEvent(event)


def acquire_single_instance_lock():
    """Acquire a lock to ensure only one instance runs. Returns socket or None."""
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        # Abstract socket (Linux) - auto-released on process exit
        sock.bind('\0main-keyboard-instance-lock')
        return sock
    except socket.error:
        return None


def main():
    # Single instance check
    lock_socket = acquire_single_instance_lock()
    if lock_socket is None:
        print("MaiN_Keyboard läuft bereits.")
        sys.exit(0)

    app = QApplication(sys.argv)
    app.setApplicationName('MaiN_Keyboard')
    app.setStyle('Fusion')
    app.setQuitOnLastWindowClosed(False)

    window = VirtualKeyboard()
    window.show()

    # System tray icon
    tray = QSystemTrayIcon()
    tray.setIcon(QIcon.fromTheme('input-keyboard'))
    tray.setToolTip('MaiN_Keyboard')

    # Tray menu
    menu = QMenu()

    show_action = QAction('Show', menu)
    show_action.triggered.connect(window.show)
    menu.addAction(show_action)

    hide_action = QAction('Hide', menu)
    hide_action.triggered.connect(window.hide)
    menu.addAction(hide_action)

    menu.addSeparator()

    # Layout submenu
    layout_menu = QMenu('Layout', menu)
    layout_group = QActionGroup(layout_menu)
    layout_group.setExclusive(True)

    for layout_id in AVAILABLE_LAYOUTS:
        layout_name = LAYOUT_NAMES.get(layout_id, layout_id.upper())
        action = QAction(layout_name, layout_menu)
        action.setCheckable(True)
        action.setChecked(layout_id == window._current_layout)
        action.triggered.connect(lambda checked, lid=layout_id: window.set_layout(lid))
        layout_group.addAction(action)
        layout_menu.addAction(action)
        window.layout_actions[layout_id] = action

    menu.addMenu(layout_menu)

    # Opacity submenu
    opacity_menu = QMenu('Opacity', menu)
    opacity_group = QActionGroup(opacity_menu)
    opacity_group.setExclusive(True)

    opacity_levels = [
        (1.0, '100%'),
        (0.9, '90%'),
        (0.8, '80%'),
        (0.7, '70%'),
        (0.6, '60%'),
        (0.5, '50%'),
    ]

    for opacity_value, opacity_name in opacity_levels:
        action = QAction(opacity_name, opacity_menu)
        action.setCheckable(True)
        action.setChecked(opacity_value == window._current_opacity)
        action.triggered.connect(lambda checked, ov=opacity_value: window.set_opacity(ov))
        opacity_group.addAction(action)
        opacity_menu.addAction(action)
        window.opacity_actions[opacity_value] = action

    menu.addMenu(opacity_menu)

    menu.addSeparator()

    quit_action = QAction('Quit', menu)
    quit_action.triggered.connect(app.quit)
    menu.addAction(quit_action)

    tray.setContextMenu(menu)
    tray.activated.connect(lambda reason: window.setVisible(not window.isVisible()) if reason == QSystemTrayIcon.ActivationReason.Trigger else None)
    tray.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
