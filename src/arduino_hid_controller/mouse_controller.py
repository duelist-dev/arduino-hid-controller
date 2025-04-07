import time
import logging
import pyautogui
from typing import Union, Tuple
from .arduino_controller import ArduinoController


class MouseController(ArduinoController):
    """Класс для эмуляции мыши через Arduino"""

    def __init__(self):
        super().__init__()
        self.__logger = logging.getLogger(__name__)
        self.__current_x = None
        self.__current_y = None
        self.__screen_width = None
        self.__screen_height = None
        self.__is_started = False

        """
        Калибровка положения
        """
        self.__set_positions()

    def __set_positions(self):
        """Инициализация позиции курсора и параметров экрана"""
        try:
            self.__screen_width, self.__screen_height = pyautogui.size()
            self.__current_x, self.__current_y = pyautogui.position()
            # Корректировка граничных значений
            self.__current_x = max(0, min(self.__current_x, self.__screen_width - 1))
            self.__current_y = max(0, min(self.__current_y, self.__screen_height - 1))
        except Exception as e:
            self.__logger.error(f"Ошибка инициализации позиции: {e}")
            # Устанавливаем значения по умолчанию
            self.__screen_width, self.__screen_height = 1920, 1080
            self.__current_x, self.__current_y = self.__screen_width // 2, self.__screen_height // 2

    def start(self) -> bool:
        """Начать эмуляцию мыши"""
        result = self._send_command("mouse", "start")
        if result:
            self.__is_started = True
        return result

    def stop(self) -> bool:
        """Остановить эмуляцию мыши"""
        result = self._send_command("mouse", "stop")
        if result:
            self.__is_started = False
        return result

    def is_started(self) -> bool:
        """Проверить, активна ли эмуляция мыши"""
        return self.__is_started

    def press(self, button: Union[str, int]) -> bool:
        """
        Нажать кнопку мыши

        Аргументы:
            button: Может быть 'left', 'right', 'middle' или код кнопки
        """
        if not self.__is_started:
            self.__logger.warning("Попытка нажать кнопку при неактивной эмуляции")
            return False

        button_str = hex(button) if isinstance(button, int) else button
        if not button_str:
            self.__logger.error("Не указана кнопка мыши")
            return False

        return self._send_command("mouse", "press", button_str)

    def release(self, button: Union[str, int]) -> bool:
        """
        Отпустить кнопку мыши

        Аргументы:
            button: Может быть 'left', 'right', 'middle' или код кнопки
        """
        if not self.__is_started:
            self.__logger.warning("Попытка отпустить кнопку при неактивной эмуляции")
            return False

        button_str = hex(button) if isinstance(button, int) else button
        if not button_str:
            self.__logger.error("Не указана кнопка мыши")
            return False

        return self._send_command("mouse", "release", button_str)

    def click(self, button: Union[str, int]) -> bool:
        """
        Кликнуть кнопкой мыши

        Аргументы:
            button: Может быть 'left', 'right', 'middle' или код кнопки
        """
        button_str = hex(button) if isinstance(button, int) else button
        return self._send_command("mouse", "click", button_str)

    def move_absolute(self, target_x: int, target_y: int, duration: float = 1.0) -> bool:
        """
        Плавное перемещение курсора в указанные координаты за заданное время

        Аргументы:
            target_x: Конечная координата X (0 - левый край экрана)
            target_y: Конечная координата Y (0 - верхний край экрана)
            duration: Время перемещения в секундах (минимум 0.01)

        Возвращает:
            bool: True если перемещение успешно, False в случае ошибки
        """
        # Проверка и корректировка координат
        if not self.__is_started:
            self.__logger.warning("Попытка перемещения при неактивной эмуляции")
            return False

        if duration <= 0:
            self.__logger.error("Длительность должна быть положительной")
            return False

        self.__set_positions()
        target_x = max(0, min(target_x, self.__screen_width - 1))
        target_y = max(0, min(target_y, self.__screen_height - 1))

        if target_x == self.__current_x and target_y == self.__current_y:
            return True

        steps = max(1, int(min(duration, 300.0) * 60))
        step_delay = duration / steps
        step_x = (target_x - self.__current_x) / steps
        step_y = (target_y - self.__current_y) / steps

        for i in range(steps):
            new_x = int(self.__current_x + step_x * (i + 1))
            new_y = int(self.__current_y + step_y * (i + 1))
            rel_x = new_x - self.__current_x
            rel_y = new_y - self.__current_y

            if rel_x != 0 or rel_y != 0:
                if not self._send_command("mouse", "move", rel_x, rel_y):
                    return False

                self.__current_x = new_x
                self.__current_y = new_y
                time.sleep(step_delay)

        return True

    def move_relative(self, x: int, y: int) -> bool:
        """
        Переместить курсор мыши (относительные координаты)

        Аргументы:
            x: Горизонтальное перемещение (положительное - вправо)
            y: Вертикальное перемещение (положительное - вниз)
        """
        if not self.__is_started:
            self.__logger.warning("Попытка перемещения при неактивной эмуляции")
            return False

        return self._send_command("mouse", "move", x, y)

    def get_position(self) -> Tuple[int, int]:
        """Получить текущие виртуальные координаты курсора"""
        return self.__current_x, self.__current_y
