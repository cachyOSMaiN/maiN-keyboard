# MaiN_Keyboard

Eine Bildschirmtastatur für KDE Plasma / Wayland, die tatsächlich funktioniert.

## Warum MaiN_Keyboard?

Bestehende Lösungen wie Onboard, Maliit oder CoreKeyboard haben unter Wayland massive Probleme:
- Fokus wird vom Textfeld gestohlen
- Tastenanschläge kommen nicht an
- Komplizierte Konfiguration nötig

**MaiN_Keyboard löst diese Probleme** durch:
- XWayland-Modus mit speziellen Window-Flags
- Kernel-Level Tastatureingabe via uinput
- Kein Fokus-Stealing - Textfelder bleiben aktiv

## Features

- **Funktioniert unter Wayland** - Verwendet uinput für zuverlässige Tastatureingabe
- **Kein Fokus-Stealing** - Textfelder bleiben beim Tippen aktiv
- **Deutsches QWERTZ-Layout** - Vollständig mit Umlauten (ä, ö, ü, ß)
- **Skalierbar** - Drei Größen: S (100%), M (120%), B (160%)
- **Monitor-Wechsel** - Aktives Fenster zwischen Monitoren verschieben
- **System Tray** - Minimiert in die Taskleiste
- **Einstellungen speichern** - Merkt sich die gewählte Größe
- **Verschiebbar** - Fenster kann frei positioniert werden

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

### Manuell

**Abhängigkeiten installieren:**
```bash
sudo pacman -S python-pyqt6 python-evdev
```

**Repository klonen:**
```bash
git clone https://github.com/cachyOSMaiN/main-keyboard.git
cd main-keyboard
```

**Installieren:**
```bash
sudo make install
```

**Oder direkt ausführen:**
```bash
python3 main.py
```

### uinput Berechtigung

MaiN_Keyboard benötigt Zugriff auf `/dev/uinput`. Falls nötig:

```bash
# Einmalig Berechtigung setzen
sudo setfacl -m u:$USER:rw /dev/uinput

# Oder permanent via udev-Regel
echo 'KERNEL=="uinput", MODE="0666"' | sudo tee /etc/udev/rules.d/99-uinput.rules
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Bedienung

| Aktion | Beschreibung |
|--------|--------------|
| **Titelleiste ziehen** | Fenster verschieben |
| **S / M / B** | Größe ändern (Small/Medium/Big) |
| **<- / ->** | Aktives Fenster zum anderen Monitor |
| **✕** | In System Tray minimieren |
| **Tray-Icon Linksklick** | Tastatur ein-/ausblenden |
| **Tray-Icon Rechtsklick** | Menü (Beenden) |

## Technische Details

- **GUI:** PyQt6
- **Eingabe:** python-evdev (uinput)
- **Display:** XWayland (für Fokus-Handling)
- **Config:** `~/.config/osk/settings.json`

## Lizenz

MIT License

## Autor

MaiN
