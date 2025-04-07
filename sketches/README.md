# Arduino HID Controller

## Description
This sketch allows you to control Arduino's keyboard and mouse (in HID mode) via serial communication. The project is designed to create virtual input devices that can be controlled from a computer.

## Requirements
- Arduino board with HID support (e.g., Arduino Leonardo, Micro, Due)
- `Keyboard.h` and `Mouse.h` libraries (included in standard Arduino IDE)

## Installation
1. Install Arduino IDE
2. Connect a compatible Arduino board
3. Copy the provided code into a new sketch
4. Upload the sketch to the board

## Command Format
Commands must be sent via Serial port in the following format:
``
device|action|arguments
``

Where:
- `device`: "keyboard" or "mouse"
- `action`: one of the supported actions for the selected device
- `arguments`: additional parameters (action-dependent)

## Supported Commands

### Keyboard Commands
| Command | Description | Example |
|---------|-------------|---------|
| `keyboard\|start\|` | Initialize keyboard | `keyboard\|start\|` |
| `keyboard\|stop\|` | Deinitialize keyboard | `keyboard\|stop\|` |
| `keyboard\|press\|key_code` | Press a key | `keyboard\|press\|A` |
| `keyboard\|release\|key_code` | Release a key | `keyboard\|release\|0x80` |
| `keyboard\|release_all\|` | Release all keys | `keyboard\|release_all\|` |
| `keyboard\|print\|text` | Print text | `keyboard\|print\|Hello` |

### Mouse Commands
| Command | Description | Example |
|---------|-------------|---------|
| `mouse\|start\|` | Initialize mouse | `mouse\|start\|` |
| `mouse\|stop\|` | Deinitialize mouse | `mouse\|stop\|` |
| `mouse\|press\|button` | Press mouse button | `mouse\|press\|MOUSE_LEFT` |
| `mouse\|release\|button` | Release mouse button | `mouse\|release\|MOUSE_RIGHT` |
| `mouse\|click\|button` | Click mouse button | `mouse\|click\|MOUSE_MIDDLE` |
| `mouse\|move\|x\|y` | Move mouse | `mouse\|move\|10\|-5` |

## Response Codes
- `True` - Command executed successfully
- `False` - Command failed with error

## Key Codes
- Characters: `A`, `B`, `1`, `!`, etc.
- Hex codes: `0x80` (must include 0x prefix)
- Mouse buttons: `MOUSE_LEFT`, `MOUSE_RIGHT`, `MOUSE_MIDDLE`

## Limitations
1. Requires HID-compatible Arduino board
2. Default serial speed: 9600 baud (modifiable in code)
3. Hex codes must use "0x" prefix

## License
MIT License
