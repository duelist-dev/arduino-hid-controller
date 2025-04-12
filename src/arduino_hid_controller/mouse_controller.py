import time
import logging
import pyautogui
from typing import Union, Tuple
from .arduino_controller import ArduinoController


class MouseController(ArduinoController):
    """Класс для эмуляции мыши через Arduino"""

    def __init__(self, arduino: ArduinoController):
        self._arduino = arduino
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
        result = self._arduino._send_command("mouse", "start")
        if result:
            self.__is_started = True
        return result

    def stop(self) -> bool:
        """Остановить эмуляцию мыши"""
        result = self._arduino._send_command("mouse", "stop")
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

        return self._arduino._send_command("mouse", "press", button_str)

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

        return self._arduino._send_command("mouse", "release", button_str)

    def click(self, button: Union[str, int]) -> bool:
        """
        Кликнуть кнопкой мыши

        Аргументы:
            button: Может быть 'left', 'right', 'middle' или код кнопки
        """
        button_str = hex(button) if isinstance(button, int) else button
        return self._arduino._send_command("mouse", "click", button_str)

    #TODO: Работает не корректно
    def move_absolute(self, target_x: int, target_y: int, duration: float = 1.0) -> bool:
        """
        Усовершенствованное перемещение с коррекцией координат и проверкой отклонений.
        Возвращает True при успешном перемещении, False при ошибке.
        """
        if not self.__is_started:
            self.__logger.warning("Попытка перемещения при неактивной эмуляции")
            return False

        if duration <= 0:
            self.__logger.error("Некорректная длительность перемещения")
            return False

        # Получаем и корректируем координаты
        self.__set_positions()
        target_x = max(0, min(int(target_x), self.__screen_width - 1))
        target_y = max(0, min(int(target_y), self.__screen_height - 1))

        # Проверяем необходимость перемещения
        if (target_x, target_y) == (self.__current_x, self.__current_y):
            return True

        # Рассчитываем общее перемещение
        total_x = target_x - self.__current_x
        total_y = target_y - self.__current_y

        # Оптимальные параметры перемещения
        steps = max(1, min(int(duration * 60), 300))  # 60 шагов/сек, макс 300 шагов
        step_delay = duration / steps
        max_deviation = 5  # Максимально допустимое отклонение в пикселях

        # Основной цикл перемещения с коррекцией
        for step in range(1, steps + 1):
            # Плавное движение с ускорением/замедлением
            progress = step / steps
            eased_progress = progress  # Можно изменить на ease-in/out функцию

            # Целевые координаты на текущем шаге
            new_x = self.__current_x + total_x * eased_progress
            new_y = self.__current_y + total_y * eased_progress

            # Относительное перемещение
            rel_x = round(new_x - self.__current_x)
            rel_y = round(new_y - self.__current_y)

            if rel_x != 0 or rel_y != 0:
                # Отправляем команду перемещения
                if not self._arduino._send_command("mouse", "move", rel_x, rel_y):
                    self.__logger.error(f"Ошибка перемещения на шаге {step}")
                    return False

                # Обновляем текущую позицию
                self.__current_x += rel_x
                self.__current_y += rel_y

                # Проверка отклонения (дополнительная страховка)
                expected_x = self.__current_x + total_x * eased_progress
                expected_y = self.__current_y + total_y * eased_progress
                deviation = ((self.__current_x - expected_x) ** 2 +
                             (self.__current_y - expected_y) ** 2) ** 0.5

                if deviation > max_deviation:
                    self.__logger.warning(f"Коррекция отклонения: {deviation:.1f} пикселей")
                    return self.move_absolute(target_x, target_y, duration / 2)

            time.sleep(step_delay)

        # Финальная коррекция
        final_rel_x = target_x - self.__current_x
        final_rel_y = target_y - self.__current_y
        if final_rel_x != 0 or final_rel_y != 0:
            success = self._arduino._send_command("mouse", "move", final_rel_x, final_rel_y)
            if success:
                self.__current_x = target_x
                self.__current_y = target_y
            return success

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

        return self._arduino._send_command("mouse", "move", x, y)

    def get_position(self) -> Tuple[int, int]:
        """Получить текущие виртуальные координаты курсора"""
        return self.__current_x, self.__current_y
