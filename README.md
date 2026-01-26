# MaiN_Keyboard

An on-screen keyboard for KDE Plasma / Wayland that actually works.

## Why MaiN_Keyboard?

Existing solutions like Onboard, Maliit or CoreKeyboard have major issues under Wayland:
- Focus gets stolen from text fields
- Keystrokes don't arrive
- Complicated configuration required

**MaiN_Keyboard solves these problems** through:
- XWayland mode with special window flags
- Kernel-level keyboard input via uinput
- No focus stealing - text fields stay active

## Features

- **Works under Wayland** - Uses uinput for reliable keyboard input
- **No focus stealing** - Text fields remain active while typing
- **German QWERTZ layout** - Complete with umlauts (ä, ö, ü, ß)
- **Scalable** - Three sizes: S (100%), M (120%), B (160%)
- **Monitor switching** - Move active window between monitors
- **System Tray** - Minimizes to taskbar
- **Saves settings** - Remembers chosen size
- **Movable** - Window can be freely positioned

## Screenshots

```
┌─────────────────────────────────────────────────────────────┐
│ MaiN_Keyboard          <- -> | S | M | B | ✕               │
├─────────────────────────────────────────────────────────────┤
│ ^ │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │ 0 │ ß │ ´ │  ⌫   │
│ Tab │ Q │ W │ E │ R │ T │ Z │ U │ I │ O │ P │ Ü │ + │  ↵  │
│ Caps │ A │ S │ D │ F │ G │ H │ J │ K │ L │ Ö │ Ä │ #      │
│  ⇧   │<│ Y │ X │ C │ V │ B │ N │ M │ , │ . │ - │    ⇧    │
│ Ctrl │ Alt │         Space         │AltGr│ ← │ ↓ │ ↑ │ → │
└─────────────────────────────────────────────────────────────┘
```

## Installation

### Arch Linux / CachyOS / Manjaro (AUR)

```bash
yay -S main-keyboard-git
```

### Manual Installation

**Install dependencies:**
```bash
sudo pacman -S python-pyqt6 python-evdev
```

**Clone repository:**
```bash
git clone https://github.com/cachyOSMaiN/maiN-keyboard.git
cd main-keyboard
```

**Install:**
```bash
sudo make install
```

**Or run directly:**
```bash
python3 main.py
```

### uinput Permission

MaiN_Keyboard requires access to `/dev/uinput`. If needed:

```bash
# Set permission once
sudo setfacl -m u:$USER:rw /dev/uinput

# Or permanently via udev rule
echo 'KERNEL=="uinput", MODE="0666"' | sudo tee /etc/udev/rules.d/99-uinput.rules
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Usage

| Action | Description |
|--------|-------------|
| **Drag title bar** | Move window |
| **S / M / B** | Change size (Small/Medium/Big) |
| **<- / ->** | Move active window to other monitor |
| **✕** | Minimize to system tray |
| **Tray icon left-click** | Show/hide keyboard |
| **Tray icon right-click** | Menu (Quit) |

## Technical Details

- **GUI:** PyQt6
- **Input:** python-evdev (uinput)
- **Display:** XWayland (for focus handling)
- **Config:** `~/.config/osk/settings.json`

## License

MIT License

## Author

MaiN
