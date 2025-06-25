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
from arduino_hid_controller import HIDController, KeyboardKey, MouseButton

# Auto-connects to Arduino (make sure sketch is uploaded)
hid = HIDController()

# Keyboard examples (no admin required)
hid.keyboard.start()
hid.keyboard.write("Hello World!")
hid.keyboard.press(KeyboardKey.F12)
# Mouse examples (admin may be required for absolute positioning)
hid.mouse.start()
hid.mouse.move_absolute(500, 300)  # Requires admin
hid.mouse.click(MouseButton.LEFT)        # Doesn't require admin

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
| `press(key)`                         | key: str/KeyboardKey | bool | Press key                  |
| `release(key)`                       | key: str/KeyboardKey | bool | Release key                |
| `press_and_release(key, delay=0.05)` | key: str/KeyboardKey, delay: float | bool | Press and release          |
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
| `press(button)`   | button: MouseButton | Press mouse button |
| `release(button)` | button: MouseButton | Release mouse button |
| `click(button)`   | button: MouseButton | Click mouse button |

#### Movement Methods
| Method | Parameters | Description |
|--------|------------|-------------|
| `move_relative(x, y)` | x: int, y: int | Relative movement |
| `move_absolute(x, y, duration=1.0)` | x: int, y: int, duration: float | Absolute movement |
| `get_position()` | - | Current coordinates |

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