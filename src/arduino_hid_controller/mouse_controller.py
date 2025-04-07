import time

import pyautogui
from typing import Union, Tuple
from .arduino_controller import ArduinoController


class MouseController(ArduinoController):
    """Класс для эмуляции мыши через Arduino"""

    def __init__(self):
        super().__init__()
        self.current_x = None
        self.current_y = None
        self.screen_width = None
        self.screen_height = None

        """
        Калибровка положения
        """
        self.__set_positions()

    def __set_positions(self):
        # Получаем разрешение экрана
        self.screen_width, self.screen_height = pyautogui.size()
        # Автоматическая калибровка начального положения
        self.current_x, self.current_y = pyautogui.position()
        # Проверка и корректировка граничных значений
        self.current_x = max(0, min(self.current_x, self.screen_width - 1))
        self.current_y = max(0, min(self.current_y, self.screen_height - 1))

    def start(self) -> bool:
        """Начать эмуляцию мыши"""
        return self._send_command("mouse", "start")

    def stop(self) -> bool:
        """Остановить эмуляцию мыши"""
        return self._send_command("mouse", "stop")

    def press(self, button: Union[str, int]) -> bool:
        """
        Нажать кнопку мыши

        Аргументы:
            button: Может быть 'left', 'right', 'middle' или код кнопки
        """
        button_str = hex(button) if isinstance(button, int) else button
        return self._send_command("mouse", "press", button_str)

    def release(self, button: Union[str, int]) -> bool:
        """
        Отпустить кнопку мыши

        Аргументы:
            button: Может быть 'left', 'right', 'middle' или код кнопки
        """
        button_str = hex(button) if isinstance(button, int) else button
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
        self.__set_positions()
        target_x = max(0, min(target_x, self.screen_width - 1))
        target_y = max(0, min(target_y, self.screen_height - 1))
        # Если координаты не изменились
        if target_x == self.current_x and target_y == self.current_y:
            return True
        # Рассчитываем перемещение
        dx = target_x - self.current_x
        dy = target_y - self.current_y
        # Рассчитываем количество шагов (60 шагов в секунду)
        steps = max(1, int(duration * 60))
        step_delay = duration / steps
        # Рассчитываем приращение на каждом шаге
        step_x = dx / steps
        step_y = dy / steps
        # Выполняем плавное перемещение
        for i in range(steps):
            # Вычисляем новые координаты
            new_x = int(self.current_x + step_x * (i + 1))
            new_y = int(self.current_y + step_y * (i + 1))
            # Вычисляем относительное перемещение
            rel_x = new_x - self.current_x
            rel_y = new_y - self.current_y
            # Отправляем команду перемещения
            if rel_x != 0 or rel_y != 0:
                success = self._send_command("mouse", "move", rel_x, rel_y)
                if not success:
                    return False
                # Обновляем текущие координаты
                self.current_x = new_x
                self.current_y = new_y
                # Задержка между шагами
                time.sleep(step_delay)
        return True

    def move_relative(self, x: int, y: int) -> bool:
        """
        Переместить курсор мыши (относительные координаты)

        Аргументы:
            x: Горизонтальное перемещение (положительное - вправо)
            y: Вертикальное перемещение (положительное - вниз)
        """
        return self._send_command("mouse", "move", x, y)

    def get_position(self) -> Tuple[int, int]:
        """Получить текущие виртуальные координаты курсора"""
        return self.current_x, self.current_y
