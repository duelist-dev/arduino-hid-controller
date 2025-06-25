# https://docs.arduino.cc/language-reference/en/functions/usb/Keyboard/keyboardModifiers/
from enum import Enum


class KeyboardKey(str, Enum):
    LEFT_CTRL = "0x80"
    LEFT_SHIFT = "0x81"
    LEFT_ALT = "0x82"
    LEFT_GUI = "0x83"
    RIGHT_CTRL = "0x84"
    RIGHT_SHIFT = "0x85"
    RIGHT_ALT = "0x86"
    RIGHT_GUI = "0x87"

    UP_ARROW = "0xDA"
    DOWN_ARROW = "0xD9"
    LEFT_ARROW = "0xD8"
    RIGHT_ARROW = "0xD7"
    BACKSPACE = "0xB2"
    TAB = "0xB3"
    RETURN = "0xB0"
    ESC = "0xB1"
    INSERT = "0xD1"
    DELETE = "0xD4"
    PAGE_UP = "0xD3"
    PAGE_DOWN = "0xD6"
    HOME = "0xD2"
    END = "0xD5"
    CAPS_LOCK = "0xC1"

    F1 = "0xC2"
    F2 = "0xC3"
    F3 = "0xC4"
    F4 = "0xC5"
    F5 = "0xC6"
    F6 = "0xC7"
    F7 = "0xC8"
    F8 = "0xC9"
    F9 = "0xCA"
    F10 = "0xCB"
    F11 = "0xCC"
    F12 = "0xCD"
    F13 = "0xF0"
    F14 = "0xF1"
    F15 = "0xF2"
    F16 = "0xF3"
    F17 = "0xF4"
    F18 = "0xF5"
    F19 = "0xF6"
    F20 = "0xF7"
    F21 = "0xF8"
    F22 = "0xF9"
    F23 = "0xFA"
    F24 = "0xFB"

    MEDIA_PLAY = "0xE0"
    MEDIA_PAUSE = "0xE1"
    MEDIA_RECORD = "0xE2"
    MEDIA_FAST_FORWARD = "0xE3"
    MEDIA_REWIND = "0xE4"
    MEDIA_NEXT = "0xE5"
    MEDIA_PREV = "0xE6"
    MEDIA_STOP = "0xE7"
    MEDIA_EJECT = "0xE8"
    MEDIA_RANDOM_PLAY = "0xE9"
    MEDIA_PLAY_PAUSE = "0xEA"
    MEDIA_PLAY_SKIP = "0xEB"
    MEDIA_VOLUME_MUTE = "0xEC"
    MEDIA_VOLUME_UP = "0xED"
    MEDIA_VOLUME_DOWN = "0xEE"
    MEDIA_BASS_BOOST = "0xEF"

    PRINT_SCREEN = "0xCE"
    SCROLL_LOCK = "0xCF"
    PAUSE = "0xD0"

    def __str__(self) -> str:
        return self.value


class MouseButton(str, Enum):
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"

    def __str__(self) -> str:
        return self.value
