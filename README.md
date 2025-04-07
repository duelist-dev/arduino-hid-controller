# Arduino HID Python Controller

## Description
Python library for controlling keyboard and mouse through Arduino in HID (Human Interface Device) mode. Provides complete control over input device emulation.

## Installation
```bash
pip install pyserial pyautogui
```

## Quick Start
```python
from arduino-hid-controller import HIDController, KEY_LEFT_CTRL, MOUSE_LEFT

hid = HIDController()  # Auto-connects to Arduino

# Keyboard control
hid.keyboard.start()
hid.keyboard.press('A')
hid.keyboard.write("Hello")

# Mouse control
hid.mouse.start()
hid.mouse.move_absolute(500, 300)
hid.mouse.click(MOUSE_LEFT)

hid.keyboard.stop()
hid.mouse.stop()
```

## Complete Documentation

### HIDController Class
Main facade class for device control.

**Attributes:**
- `keyboard` - KeyboardController instance
- `mouse` - MouseController instance

### KeyboardController Class

#### Core Methods
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `start()` | - | bool | Initialize keyboard |
| `stop()` | - | bool | Stop emulation |
| `press(key)` | key: str/int | bool | Press key |
| `release(key)` | key: str/int | bool | Release key |
| `press_and_release(key, delay=0.05)` | key: str/int, delay: float | bool | Press and release |
| `release_all()` | - | bool | Release all keys |

#### Special Methods
| Method | Parameters | Description |
|--------|------------|-------------|
| `key_combo(keys, delay=0.05)` | keys: list, delay: float | Key combination |
| `write(text)` | text: str | Type text |

### MouseController Class

#### Core Methods
| Method | Parameters | Description |
|--------|------------|-------------|
| `start()` | - | Initialize mouse |
| `stop()` | - | Stop emulation |
| `press(button)` | button: str | Press mouse button |
| `release(button)` | button: str | Release mouse button |
| `click(button)` | button: str | Click mouse button |

#### Movement Methods
| Method | Parameters | Description |
|--------|------------|-------------|
| `move_relative(x, y)` | x: int, y: int | Relative movement |
| `move_absolute(x, y, duration=1.0)` | x: int, y: int, duration: float | Absolute movement |
| `get_position()` | - | Current coordinates |

## Constants

### Key Modifiers
```python
KEY_LEFT_CTRL = "0x80"
KEY_LEFT_SHIFT = "0x81"
KEY_LEFT_ALT = "0x82"
KEY_LEFT_GUI = "0x83"  # Windows/Command
```

### Special Keys
```python
KEY_UP_ARROW = "0xDA"
KEY_DOWN_ARROW = "0xD9"
KEY_BACKSPACE = "0xB2"
KEY_ENTER = "0xB0"
```

### Mouse Buttons
```python
MOUSE_LEFT = 'left'
MOUSE_RIGHT = 'right'
MOUSE_MIDDLE = 'middle'
```

## Usage Examples

### Hotkey Emulation
```python
# Ctrl+Alt+Delete
hid.keyboard.key_combo([KEY_LEFT_CTRL, KEY_LEFT_ALT, KEY_DELETE])

# Alt+Tab
hid.keyboard.press(KEY_LEFT_ALT)
hid.keyboard.press_and_release(KEY_TAB)
hid.keyboard.release(KEY_LEFT_ALT)
```

### Mouse Automation
```python
# Square movement pattern
points = [(100,100), (100,200), (200,200), (200,100)]
for x,y in points:
    hid.mouse.move_absolute(x, y, duration=0.5)
    hid.mouse.click(MOUSE_LEFT)
```

## Error Handling
All methods return `True` on success or `False` on failure. Possible exceptions:
- `RuntimeError` - connection issues
- `ValueError` - invalid arguments
- `SerialException` - communication errors

## System Requirements
- Python 3.7+
- Dependencies:
  - pyserial >= 3.5
  - pyautogui >= 0.9.50 (for screen resolution detection)
- Hardware:
  - Arduino Leonardo/Micro
  - HID controller firmware

## License
MIT License