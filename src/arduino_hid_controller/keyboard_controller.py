import time
import logging
from typing import Union, Iterable
from .arduino_controller import ArduinoController


class KeyboardController(ArduinoController):
    """Класс для эмуляции клавиатуры через Arduino"""

    def __init__(self):
        super().__init__()
        self.__logger = logging.getLogger(__name__)
        self.__is_started = False

    def start(self) -> bool:
        """Начать эмуляцию клавиатуры"""
        result = self._send_command("keyboard", "start")
        if result:
            self.__is_started = True
        return result

    def stop(self) -> bool:
        """Остановить эмуляцию клавиатуры"""
        result = self._send_command("keyboard", "stop")
        if result:
            self.__is_started = False
        return result

    def is_started(self) -> bool:
        """Проверить, активна ли эмуляция клавиатуры"""
        return self.__is_started

    def press(self, key: Union[str, int]) -> bool:
        """
        Нажать клавишу

        Аргументы:
            key: Символ (например, 'a') или HID-код (например, 0x04 для 'a')
        """
        if not self.__is_started:
            self.__logger.warning("Попытка нажать клавишу при неактивной эмуляции")
            return False

        key_str = hex(key) if isinstance(key, int) else key
        if not key_str:
            self.__logger.error("Не указана клавиша для нажатия")
        return self._send_command("keyboard", "press", key_str)

    def release(self, key: Union[str, int]) -> bool:
        """
        Отпустить клавишу

        Аргументы:
            key: Символ (например, 'a') или HID-код (например, 0x04 для 'a')
        """
        if not self.__is_started:
            self.__logger.warning("Попытка отпустить клавишу при неактивной эмуляции")
            return False

        key_str = hex(key) if isinstance(key, int) else key
        if not key_str:
            self.__logger.error("Не указана клавиша для отпускания")
            return False
        return self._send_command("keyboard", "release", key_str)

    def press_and_release(self, key: Union[str, int], delay: float = 0.05) -> bool:
        """
        Нажать и отпустить клавишу с заданной задержкой

        Аргументы:
            key: Символ (например, 'a') или HID-код (например, 0x04 для 'a')
            delay: Задержка в секундах между нажатием и отпусканием (по умолчанию 0.05)

        Возвращает:
            True если обе операции успешны, иначе False
        """
        pressed = self.press(key)
        if not pressed:
            return False
        time.sleep(delay)
        released = self.release(key)
        if not released:
            # Попытаемся отпустить клавишу в любом случае, даже если release вернул ошибку
            self.release(key)  # Повторная попытка
            return False

        return True

    def key_combo(self, keys: Iterable[Union[str, int]], delay: float = 0.05) -> bool:
        """
        Выполнить комбинацию клавиш (нажать все клавиши одновременно, затем отпустить)

        Аргументы:
            keys: Итерируемый объект с клавишами (символы или HID-коды)
            delay: Задержка в секундах перед отпусканием клавиш (по умолчанию 0.05)

        Возвращает:
            True если все клавиши были успешно нажаты, иначе False

        Пример:
            # CTRL+ALT+DELETE
            keyboard.key_combo([KEY_LEFT_CTRL, KEY_LEFT_ALT, KEY_DELETE])
        """
        if not keys:
            self.__logger.error("Пустой список клавиш для комбинации")
            return False
        success = True
        # Нажимаем все клавиши по очереди
        for key in keys:
            if not self.press(key):
                success = False
            time.sleep(0.01)  # небольшая задержка между нажатиями
        # Ждем указанную задержку
        time.sleep(delay)
        # Отпускаем все клавиши
        self.release_all()
        return success

    def release_all(self) -> bool:
        """Отпустить все клавиши"""
        if not self.__is_started:
            self.__logger.warning("Попытка отпустить все клавиши при неактивной эмуляции")
            return False
        return self._send_command("keyboard", "release_all")

    def write(self, text: str) -> bool:
        """
        Напечатать текст (символьный ввод)

        Аргументы:
            text: Текст для ввода
        """
        if not self.__is_started:
            self.__logger.warning("Попытка отправить текст при неактивной эмуляции")
            return False

        if not text:
            self.__logger.warning("Попытка отправить пустой текст")
            return False
        return self._send_command("keyboard", "print", text)
