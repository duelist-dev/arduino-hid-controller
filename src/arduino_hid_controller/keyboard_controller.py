import time
import logging
from typing import Union, Iterable, Optional
from constants import KeyboardKey
from .arduino_controller import ArduinoController


class KeyboardController:
    """Класс для эмуляции клавиатуры через Arduino"""
    def __init__(self, arduino: ArduinoController):
        self._arduino = arduino
        self.__logger = logging.getLogger(__name__)
        self.__is_started = False

    def start(self) -> bool:
        result = self._arduino._send_command("keyboard", "start")
        self.__is_started = result
        return result

    def stop(self) -> bool:
        result = self._arduino._send_command("keyboard", "stop")
        self.__is_started = not result
        return result

    def is_started(self) -> bool:
        return self.__is_started

    def __prepare_key(self, key: Union[str, KeyboardKey]) -> Optional[str]:
        if not self.__is_started:
            self.__logger.warning("Действие при неактивной эмуляции клавиатуры")
            return None
        if key is None:
            self.__logger.error("Клавиша не указана")
            return None
        return str(key)

    def press(self, key: Union[str, KeyboardKey]) -> bool:
        key_str = self.__prepare_key(key)
        return self._arduino._send_command("keyboard", "press", key_str) if key_str else False

    def release(self, key: Union[str, KeyboardKey]) -> bool:
        key_str = self.__prepare_key(key)
        return self._arduino._send_command("keyboard", "release", key_str) if key_str else False

    def press_and_release(self, key: Union[str, KeyboardKey], delay: float = 0.05) -> bool:
        if not self.press(key):
            self.__logger.warning(f"Не удалось нажать клавишу: {key}")
            return False
        time.sleep(delay)
        return self.release(key)

    def key_combo(self, keys: Iterable[Union[str, KeyboardKey]], delay: float = 0.05) -> bool:
        if not keys:
            self.__logger.error("Пустой список клавиш для комбинации")
            return False

        success = True
        for key in keys:
            if not self.press(key):
                self.__logger.warning(f"Ошибка при нажатии клавиши: {key}")
                success = False
            time.sleep(0.01)

        time.sleep(delay)
        self.release_all()
        return success

    def release_all(self) -> bool:
        if not self.__is_started:
            self.__logger.warning("Попытка отпустить все клавиши при неактивной эмуляции")
            return False
        return self._arduino._send_command("keyboard", "release_all")

    def write(self, text: str) -> bool:
        if not self.__is_started:
            self.__logger.warning("Попытка отправить текст при неактивной эмуляции")
            return False
        if not text:
            self.__logger.warning("Попытка отправить пустой текст")
            return False
        return self._arduino._send_command("keyboard", "print", text)
