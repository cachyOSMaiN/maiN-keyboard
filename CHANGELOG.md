# Changelog

## Unreleased

### Fixed
- **`make install` no longer fails**: The `install` target built the `/usr/bin/main-keyboard` launcher with a shell heredoc, which is invalid in a Makefile (recipe lines need tabs, and each line runs in its own shell — so the heredoc body was never seen). This caused `*** missing separator. Stop.`. The launcher is now written with a single-line `printf` (and `exec`s `python3` so no bash parent lingers).

## v1.2.0 (2026-01-27)

### Added
- **New dark design**: iOS-style buttons with 3D shadow effect and rounded corners
- **Opacity setting**: Adjustable transparency (50%-100%) via system tray menu
- **Window move indicator**: Icon between monitor switch buttons for better UX

### Changed
- Darker background color (#131315) for better contrast
- Improved button styling with bottom shadow for depth
- Adjusted default keyboard position (58px from bottom)
- Tray menu now in English

## v1.1.0 (2026-01-26)

### Added
- **Single instance enforcement**: The application now prevents multiple instances from running simultaneously. If you try to launch MaiN_Keyboard while it's already running, it will display a message and exit gracefully.

## v1.0.0 (2026-01-26)

### Initial Release
- On-screen keyboard for KDE Plasma / Wayland
- German QWERTZ layout with umlauts
- Scalable interface (S/M/B sizes)
- Monitor switching functionality
- System tray integration
- No focus stealing from text fields
- Settings persistence
