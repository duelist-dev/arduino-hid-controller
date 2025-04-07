# Arduino HID Python Controller

## Description
Python library for controlling keyboard and mouse through Arduino in HID (Human Interface Device) mode. Provides complete control over input device emulation.

## Prerequisites

### 1. Upload Arduino Sketch
Before using this library, you must upload the HID controller sketch to your Arduino:

1. Download the sketch file:
   - [arduino-hid.ino](https://github.com/duelist-dev/arduino-hid-controller/blob/main/sketches/adruino-hid.ino)

2. Open the sketch in Arduino IDE

3. Select your board type:
   - Tools → Board → "Arduino Leonardo" (or "Arduino Micro")

4. Select the correct port:
   - Tools → Port → (select your Arduino's port)

5. Upload the sketch:
   - Click the "Upload" button or press Ctrl+U


### 2. Install Python Package
```bash
pip install arduino-hid-controller
```

### 3. Administrator Privileges
Some mouse functions (particularly absolute positioning) require administrator privileges:

- **Windows**: Right-click → "Run as Administrator"
- **Linux/Mac**: Use `sudo` (note: this may require GUI permissions)

```bash
# Linux/Mac example
sudo python your_script.py
```

## Quick Start
```python
from arduino_hid_controller import HIDController, KEY_LEFT_CTRL, MOUSE_LEFT

# Auto-connects to Arduino (make sure sketch is uploaded)
hid = HIDController()

# Keyboard examples (no admin required)
hid.keyboard.start()
hid.keyboard.write("Hello World!")

# Mouse examples (admin may be required for absolute positioning)
hid.mouse.start()
hid.mouse.move_absolute(500, 300)  # Requires admin
hid.mouse.click(MOUSE_LEFT)        # Doesn't require admin

# Cleanup
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
| Method                               | Parameters | Returns | Description                |
|--------------------------------------|------------|---------|----------------------------|
| `start()`                            | - | bool | Initialize keyboard        |
| `stop()`                             | - | bool | Stop emulation             |
| `is_started()`                       | - | bool | Check is started emulation |
| `press(key)`                         | key: str/int | bool | Press key                  |
| `release(key)`                       | key: str/int | bool | Release key                |
| `press_and_release(key, delay=0.05)` | key: str/int, delay: float | bool | Press and release          |
| `release_all()`                      | - | bool | Release all keys           |

#### Special Methods
| Method | Parameters | Description |
|--------|------------|-------------|
| `key_combo(keys, delay=0.05)` | keys: list, delay: float | Key combination |
| `write(text)` | text: str | Type text |

### MouseController Class

#### Core Methods
| Method            | Parameters | Description |
|-------------------|------------|-------------|
| `start()`         | - | Initialize mouse |
| `stop()`          | - | Stop emulation |
| `is_started()`    | - | bool | Check is started emulation |
| `press(button)`   | button: str | Press mouse button |
| `release(button)` | button: str | Release mouse button |
| `click(button)`   | button: str | Click mouse button |

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
KEY_LEFT_GUI = "0x83"  # Windows/Command key
KEY_RIGHT_CTRL = "0x84"
KEY_RIGHT_SHIFT = "0x85"
KEY_RIGHT_ALT = "0x86"
KEY_RIGHT_GUI = "0x87"  # Windows/Command key
```

### Special Keys
```python
KEY_UP_ARROW = "0xDA"
KEY_DOWN_ARROW = "0xD9"
KEY_LEFT_ARROW = "0xD8"
KEY_RIGHT_ARROW = "0xD7"
KEY_BACKSPACE = "0xB2"
KEY_TAB = "0xB3"
KEY_RETURN = "0xB0"
KEY_ESC = "0xB1"
KEY_INSERT = "0xD1"
KEY_DELETE = "0xD4"
KEY_PAGE_UP = "0xD3"
KEY_PAGE_DOWN = "0xD6"
KEY_HOME = "0xD2"
KEY_END = "0xD5"
KEY_CAPS_LOCK = "0xC1"
```

### Function Keys
```python
KEY_F1 = "0xC2"
KEY_F2 = "0xC3"
KEY_F3 = "0xC4"
KEY_F4 = "0xC5"
KEY_F5 = "0xC6"
KEY_F6 = "0xC7"
KEY_F7 = "0xC8"
KEY_F8 = "0xC9"
KEY_F9 = "0xCA"
KEY_F10 = "0xCB"
KEY_F11 = "0xCC"
KEY_F12 = "0xCD"
KEY_F13 = "0xF0"
KEY_F14 = "0xF1"
KEY_F15 = "0xF2"
KEY_F16 = "0xF3"
KEY_F17 = "0xF4"
KEY_F18 = "0xF5"
KEY_F19 = "0xF6"
KEY_F20 = "0xF7"
KEY_F21 = "0xF8"
KEY_F22 = "0xF9"
KEY_F23 = "0xFA"
KEY_F24 = "0xFB"
```

### Media keys
```python
KEY_MEDIA_PLAY = "0xE0"
KEY_MEDIA_PAUSE = "0xE1"
KEY_MEDIA_RECORD = "0xE2"
KEY_MEDIA_FAST_FORWARD = "0xE3"
KEY_MEDIA_REWIND = "0xE4"
KEY_MEDIA_NEXT = "0xE5"
KEY_MEDIA_PREV = "0xE6"
KEY_MEDIA_STOP = "0xE7"
KEY_MEDIA_EJECT = "0xE8"
KEY_MEDIA_RANDOM_PLAY = "0xE9"
KEY_MEDIA_PLAY_PAUSE = "0xEA"
KEY_MEDIA_PLAY_SKIP = "0xEB"
KEY_MEDIA_VOLUME_MUTE = "0xEC"
KEY_MEDIA_VOLUME_UP = "0xED"
KEY_MEDIA_VOLUME_DOWN = "0xEE"
KEY_MEDIA_BASS_BOOST = "0xEF"
```
### Function control keys
```python
KEY_PRINT_SCREEN = "0xCE"
KEY_SCROLL_LOCK = "0xCF"
KEY_PAUSE = "0xD0"
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

## Function-Specific Requirements

| Function | Requires Admin | Notes |
|----------|---------------|-------|
| `move_absolute()` | Yes | Needs screen access |
| `get_position()` | Yes | Needs screen access |
| `move_relative()` | No | - |
| All keyboard functions | No | - |

## Troubleshooting

### Permission Errors
If you get errors about screen access:
1. On Windows, run as Administrator
2. On Linux/Mac:
   ```bash
   sudo python your_script.py
   ```
   or configure permanent permissions:
   ```bash
   sudo usermod -a -G input $USER  # For mouse access
   sudo reboot
   ```
   
### Arduino Not Detected
1. Verify the sketch uploaded successfully
2. Check your USB cable (some cables are power-only)
3. Ensure you selected the correct board type in Arduino IDE

## License
MIT License