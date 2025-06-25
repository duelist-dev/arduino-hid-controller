#include <Keyboard.h>
#include <Mouse.h>

const char COMMAND_SEPARATOR = '|';

enum Device {
    DEVICE_KEYBOARD,
    DEVICE_MOUSE,
    DEVICE_UNKNOWN
};

enum ActionKeyboard {
    ACTION_KEYBOARD_START,
    ACTION_KEYBOARD_STOP,
    ACTION_KEYBOARD_PRESS,
    ACTION_KEYBOARD_RELEASE,
    ACTION_KEYBOARD_RELEASE_ALL,
    ACTION_KEYBOARD_PRINT,
    ACTION_KEYBOARD_UNKNOWN
};

enum ActionMouse {
    ACTION_MOUSE_START,
    ACTION_MOUSE_STOP,
    ACTION_MOUSE_PRESS,
    ACTION_MOUSE_RELEASE,
    ACTION_MOUSE_CLICK,
    ACTION_MOUSE_MOVE,
    ACTION_MOUSE_UNKNOWN
};

void setup() {
    Serial.begin(9600);
    Serial.setTimeout(50);
    while (Serial.available()) Serial.read(); // Очистить буфер
}

void loop() {
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        bool result = executeCommand(command);
        Serial.println(result ? F("True") : F("False"));
    }
}

Device parseDevice(const String& deviceStr) {
    if (deviceStr == F("keyboard")) return DEVICE_KEYBOARD;
    if (deviceStr == F("mouse")) return DEVICE_MOUSE;
    return DEVICE_UNKNOWN;
}

ActionKeyboard parseActionKeyboard(const String& actionStr) {
    if (actionStr == F("start")) return ACTION_KEYBOARD_START;
    if (actionStr == F("stop")) return ACTION_KEYBOARD_STOP;
    if (actionStr == F("press")) return ACTION_KEYBOARD_PRESS;
    if (actionStr == F("release")) return ACTION_KEYBOARD_RELEASE;
    if (actionStr == F("release_all")) return ACTION_KEYBOARD_RELEASE_ALL;
    if (actionStr == F("print")) return ACTION_KEYBOARD_PRINT;
    return ACTION_KEYBOARD_UNKNOWN;
}

ActionMouse parseActionMouse(const String& actionStr) {
    if (actionStr == F("start")) return ACTION_MOUSE_START;
    if (actionStr == F("stop")) return ACTION_MOUSE_STOP;
    if (actionStr == F("press")) return ACTION_MOUSE_PRESS;
    if (actionStr == F("release")) return ACTION_MOUSE_RELEASE;
    if (actionStr == F("click")) return ACTION_MOUSE_CLICK;
    if (actionStr == F("move")) return ACTION_MOUSE_MOVE;
    return ACTION_MOUSE_UNKNOWN;
}

uint8_t parseMouseButton(const String& button) {
    if (button == "left") return MOUSE_LEFT;
    if (button == "right") return MOUSE_RIGHT;
    if (button == "middle") return MOUSE_MIDDLE;

    Serial.println(F("Error: Unknown mouse button"));
    return 0;
}

bool executeCommand(String command) {
    if (command.length() == 0) {
        Serial.println(F("Error: Empty command"));
        return false;
    }
    if (!validateCommand(command)) {
        Serial.println(F("Error: Invalid command format"));
        return false;
    }

    String deviceStr = separateString(command, COMMAND_SEPARATOR, 0, false);
    String actionStr = separateString(command, COMMAND_SEPARATOR, 1, false);
    String args = separateString(command, COMMAND_SEPARATOR, 2, true);

    Device device = parseDevice(deviceStr);
    if (device == DEVICE_UNKNOWN) {
        Serial.println(F("Error: Unknown device"));
        return false;
    }

    switch (device) {
        case DEVICE_KEYBOARD: {
            ActionKeyboard actionKeyboard = parseActionKeyboard(actionStr);
            if (actionKeyboard == ACTION_KEYBOARD_UNKNOWN) {
                Serial.println(F("Error: Unknown keyboard action"));
                return false;
            }
            return handleKeyboard(actionKeyboard, args);
        }
        case DEVICE_MOUSE: {
            ActionMouse actionMouse = parseActionMouse(actionStr);
            if (actionMouse == ACTION_MOUSE_UNKNOWN) {
                Serial.println(F("Error: Unknown mouse action"));
                return false;
            }
            return handleMouse(actionMouse, args);
        }
        default:
            return false;
    }
}

bool handleMouse(ActionMouse action, const String& args) {
    switch (action) {
        case ACTION_MOUSE_START:
            Mouse.begin();
            return true;
        case ACTION_MOUSE_STOP:
            Mouse.end();
            return true;
        case ACTION_MOUSE_PRESS:
        case ACTION_MOUSE_RELEASE:
        case ACTION_MOUSE_CLICK: {
            if (args.length() == 0) {
                Serial.println(F("Error: Missing mouse key"));
                return false;
            }
            uint8_t btn = parseMouseButton(args);
            if (btn == 0) return false;
            Mouse.press(btn);
            return true;
        }
        case ACTION_MOUSE_MOVE: {
            if (args.indexOf(COMMAND_SEPARATOR) == -1) {
                Serial.println(F("Error: Missing mouse coordinates"));
                return false;
            }
            int x = separateString(args, COMMAND_SEPARATOR, 0, false).toInt();
            int y = separateString(args, COMMAND_SEPARATOR, 1, false).toInt();
            Mouse.move(x, y, 0);
            delay(1); // небольшая пауза для стабильности
            return true;
        }
        default:
            return false;
    }
}

bool handleKeyboard(ActionKeyboard action, const String& args) {
    switch (action) {
        case ACTION_KEYBOARD_START:
            Keyboard.begin();
            return true;
        case ACTION_KEYBOARD_STOP:
            Keyboard.end();
            return true;
        case ACTION_KEYBOARD_PRESS:
        case ACTION_KEYBOARD_RELEASE: {
            if (args.length() == 0) {
                Serial.println(F("Error: Missing keyboard key"));
                return false;
            }
            char key_code = parseKey(args);
            if (key_code == '\0') return false;

            if (action == ACTION_KEYBOARD_PRESS) Keyboard.press(key_code);
            else Keyboard.release(key_code);

            return true;
        }
        case ACTION_KEYBOARD_RELEASE_ALL:
            Keyboard.releaseAll();
            return true;
        case ACTION_KEYBOARD_PRINT:
            if (args.length() == 0) {
                Serial.println(F("Error: Missing text to print"));
                return false;
            }
            Keyboard.print(args);
            return true;
        default:
            return false;
    }
}

bool validateCommand(const String& command) {
    int sepCount = 0;
    for (unsigned i = 0; i < command.length(); i++) {
        if (command[i] == COMMAND_SEPARATOR) sepCount++;
    }
    return sepCount >= 2;
}

char parseKey(const String& key) {
    String trimmed = key;
    trimmed.trim();

    if (trimmed.length() == 0) {
        Serial.println(F("Error: Empty key"));
        return '\0';
    }

    if (trimmed.startsWith("0x")) {
        long val = strtol(trimmed.c_str(), nullptr, 16);
        if (val < 0 || val > 255) {
            Serial.println(F("Error: Key code out of range"));
            return '\0';
        }
        return (char)val;
    }

    return trimmed[0];
}

String separateString(const String& data, char separator, int index, bool getRemaining) {
    if (index < 0) return "";
    int found = 0;
    int strIndex[] = {0, -1};
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            if (getRemaining && found == index) {
                strIndex[0] = strIndex[1] + 1;
                strIndex[1] = maxIndex + 1;
                return data.substring(strIndex[0], strIndex[1]);
            }
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = i;
            if (i == maxIndex && data.charAt(i) != separator) {
                strIndex[1] = i + 1;
            }
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}
