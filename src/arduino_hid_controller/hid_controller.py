from .arduino_controller import ArduinoController
from .keyboard_controller import KeyboardController
from .mouse_controller import MouseController


class HIDController:
    """Фасадный класс для управления HID-устройствами"""

    def __init__(self, port: str = None, auto_reconnect: bool = True):
        """
        Инициализация контроллера HID-устройств
        """
        self._arduino = ArduinoController(port=port, auto_reconnect=auto_reconnect)
        self.keyboard = KeyboardController(self._arduino)
        self.mouse = MouseController(self._arduino)

    @property
    def arduino(self):
        return self._arduino

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self._arduino, '__exit__'):
            self._arduino.__exit__(exc_type, exc_val, exc_tb)
