from .arduino_controller import ArduinoController
from .keyboard_controller import KeyboardController
from .mouse_controller import MouseController


class HIDController:
    """Фасадный класс для управления HID-устройствами"""

    def __init__(self):
        """
        Инициализация контроллера HID-устройств
        """
        self._arduino = ArduinoController()
        self.keyboard = KeyboardController(self._arduino)
        self.mouse = MouseController(self._arduino)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self
