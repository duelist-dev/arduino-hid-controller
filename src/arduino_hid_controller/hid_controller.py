from .keyboard_controller import KeyboardController
from .mouse_controller import MouseController


class HIDController:
    """Фасадный класс для управления HID-устройствами"""

    def __init__(self):
        """
        Инициализация контроллера HID-устройств
        """
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
