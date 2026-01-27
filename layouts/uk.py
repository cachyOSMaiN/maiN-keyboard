"""UK QWERTY keyboard layout definition."""

from evdev import ecodes

# Key definitions: (normal_char, shift_char, keycode)
# For special keys, normal_char is the display label

LAYOUT = [
    # Row 1: Number row
    [
        ('`', '¬', ecodes.KEY_GRAVE),
        ('1', '!', ecodes.KEY_1),
        ('2', '"', ecodes.KEY_2),
        ('3', '£', ecodes.KEY_3),
        ('4', '$', ecodes.KEY_4),
        ('5', '%', ecodes.KEY_5),
        ('6', '^', ecodes.KEY_6),
        ('7', '&', ecodes.KEY_7),
        ('8', '*', ecodes.KEY_8),
        ('9', '(', ecodes.KEY_9),
        ('0', ')', ecodes.KEY_0),
        ('-', '_', ecodes.KEY_MINUS),
        ('=', '+', ecodes.KEY_EQUAL),
        ('⌫', '⌫', ecodes.KEY_BACKSPACE),
    ],
    # Row 2: QWERTY top row
    [
        ('Tab', 'Tab', ecodes.KEY_TAB),
        ('q', 'Q', ecodes.KEY_Q),
        ('w', 'W', ecodes.KEY_W),
        ('e', 'E', ecodes.KEY_E),
        ('r', 'R', ecodes.KEY_R),
        ('t', 'T', ecodes.KEY_T),
        ('y', 'Y', ecodes.KEY_Y),
        ('u', 'U', ecodes.KEY_U),
        ('i', 'I', ecodes.KEY_I),
        ('o', 'O', ecodes.KEY_O),
        ('p', 'P', ecodes.KEY_P),
        ('[', '{', ecodes.KEY_LEFTBRACE),
        (']', '}', ecodes.KEY_RIGHTBRACE),
        ('↵', '↵', ecodes.KEY_ENTER),
    ],
    # Row 3: Home row
    [
        ('Caps', 'Caps', ecodes.KEY_CAPSLOCK),
        ('a', 'A', ecodes.KEY_A),
        ('s', 'S', ecodes.KEY_S),
        ('d', 'D', ecodes.KEY_D),
        ('f', 'F', ecodes.KEY_F),
        ('g', 'G', ecodes.KEY_G),
        ('h', 'H', ecodes.KEY_H),
        ('j', 'J', ecodes.KEY_J),
        ('k', 'K', ecodes.KEY_K),
        ('l', 'L', ecodes.KEY_L),
        (';', ':', ecodes.KEY_SEMICOLON),
        ("'", '@', ecodes.KEY_APOSTROPHE),
        ('#', '~', ecodes.KEY_BACKSLASH),
    ],
    # Row 4: Bottom letter row
    [
        ('⇧', '⇧', ecodes.KEY_LEFTSHIFT),
        ('\\', '|', ecodes.KEY_102ND),
        ('z', 'Z', ecodes.KEY_Z),
        ('x', 'X', ecodes.KEY_X),
        ('c', 'C', ecodes.KEY_C),
        ('v', 'V', ecodes.KEY_V),
        ('b', 'B', ecodes.KEY_B),
        ('n', 'N', ecodes.KEY_N),
        ('m', 'M', ecodes.KEY_M),
        (',', '<', ecodes.KEY_COMMA),
        ('.', '>', ecodes.KEY_DOT),
        ('/', '?', ecodes.KEY_SLASH),
        ('⇧', '⇧', ecodes.KEY_RIGHTSHIFT),
    ],
    # Row 5: Bottom row with space
    [
        ('Ctrl', 'Ctrl', ecodes.KEY_LEFTCTRL),
        ('Alt', 'Alt', ecodes.KEY_LEFTALT),
        ('Space', 'Space', ecodes.KEY_SPACE),
        ('AltGr', 'AltGr', ecodes.KEY_RIGHTALT),
        ('←', '←', ecodes.KEY_LEFT),
        ('↓', '↓', ecodes.KEY_DOWN),
        ('↑', '↑', ecodes.KEY_UP),
        ('→', '→', ecodes.KEY_RIGHT),
    ],
]

# Special keys that toggle or act as modifiers
MODIFIER_KEYS = {
    ecodes.KEY_LEFTSHIFT,
    ecodes.KEY_RIGHTSHIFT,
    ecodes.KEY_LEFTCTRL,
    ecodes.KEY_LEFTALT,
    ecodes.KEY_RIGHTALT,
    ecodes.KEY_CAPSLOCK,
}

# Keys that should have wider buttons
WIDE_KEYS = {
    ecodes.KEY_BACKSPACE: 1.5,
    ecodes.KEY_TAB: 1.5,
    ecodes.KEY_ENTER: 1.5,
    ecodes.KEY_CAPSLOCK: 1.75,
    ecodes.KEY_LEFTSHIFT: 1.25,
    ecodes.KEY_RIGHTSHIFT: 2.25,
    ecodes.KEY_LEFTCTRL: 1.25,
    ecodes.KEY_LEFTALT: 1.25,
    ecodes.KEY_SPACE: 6.0,
    ecodes.KEY_RIGHTALT: 1.25,
}
