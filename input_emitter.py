"""Input emitter using python-evdev and uinput for Wayland compatibility."""

import evdev
from evdev import UInput, ecodes


class InputEmitter:
    """Emulates keyboard input via uinput device."""

    def __init__(self):
        """Create a virtual keyboard device."""
        # Define capabilities - all standard keyboard keys
        capabilities = {
            ecodes.EV_KEY: list(range(1, 256)),  # All key codes
        }

        self.device = UInput(
            capabilities,
            name='Virtual-OSK',
            vendor=0x1234,
            product=0x5678,
        )

        # Track active modifiers
        self._active_modifiers = set()

    def send_key(self, keycode: int, with_shift: bool = False):
        """
        Send a single key press and release.

        Args:
            keycode: The evdev keycode to send
            with_shift: Whether to hold shift during the keypress
        """
        # Press shift if needed and not already active
        if with_shift and ecodes.KEY_LEFTSHIFT not in self._active_modifiers:
            self.device.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 1)
            self.device.syn()

        # Key press
        self.device.write(ecodes.EV_KEY, keycode, 1)
        self.device.syn()

        # Key release
        self.device.write(ecodes.EV_KEY, keycode, 0)
        self.device.syn()

        # Release shift if we pressed it
        if with_shift and ecodes.KEY_LEFTSHIFT not in self._active_modifiers:
            self.device.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 0)
            self.device.syn()

    def press_modifier(self, keycode: int):
        """Press and hold a modifier key."""
        if keycode not in self._active_modifiers:
            self._active_modifiers.add(keycode)
            self.device.write(ecodes.EV_KEY, keycode, 1)
            self.device.syn()

    def release_modifier(self, keycode: int):
        """Release a held modifier key."""
        if keycode in self._active_modifiers:
            self._active_modifiers.discard(keycode)
            self.device.write(ecodes.EV_KEY, keycode, 0)
            self.device.syn()

    def toggle_modifier(self, keycode: int) -> bool:
        """
        Toggle a modifier key state.

        Returns:
            bool: True if modifier is now active, False if released
        """
        if keycode in self._active_modifiers:
            self.release_modifier(keycode)
            return False
        else:
            self.press_modifier(keycode)
            return True

    def is_modifier_active(self, keycode: int) -> bool:
        """Check if a modifier is currently active."""
        return keycode in self._active_modifiers

    def release_all_modifiers(self):
        """Release all held modifier keys."""
        for keycode in list(self._active_modifiers):
            self.release_modifier(keycode)

    def close(self):
        """Clean up the uinput device."""
        self.release_all_modifiers()
        self.device.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
