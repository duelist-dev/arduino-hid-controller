import time
import logging
import pyautogui
import ctypes
from typing import Union, Tuple
from constants import MouseButton
from .arduino_controller import ArduinoController


def get_real_screen_resolution() -> Tuple[int, int]:
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


class MouseController:
    """Класс для эмуляции мыши через Arduino"""

    MAX_RETRY = 3  # Константа для ограничения попыток перемещения

    def __init__(self, arduino: ArduinoController):
        self._arduino = arduino
        self.__logger = logging.getLogger(__name__)
        self.__current_x = None
        self.__current_y = None
        self.__screen_width = None
        self.__screen_height = None
        self.__is_started = False
        self.__set_positions()

    def __set_positions(self):
        try:
            self.__screen_width, self.__screen_height = get_real_screen_resolution()
            self.__current_x, self.__current_y = pyautogui.position()
            self.__current_x = max(0, min(self.__current_x, self.__screen_width - 1))
            self.__current_y = max(0, min(self.__current_y, self.__screen_height - 1))
        except Exception as e:
            self.__logger.error(f"Ошибка инициализации позиции: {e}")
            self.__screen_width, self.__screen_height = 1920, 1080
            self.__current_x, self.__current_y = 960, 540

    def start(self) -> bool:
        result = self._arduino._send_command("mouse", "start")
        self.__is_started = result
        return result

    def stop(self) -> bool:
        result = self._arduino._send_command("mouse", "stop")
        self.__is_started = not result
        return result

    def is_started(self) -> bool:
        return self.__is_started

    def press(self, button: MouseButton) -> bool:
        if not self.__is_started:
            self.__logger.warning("Попытка нажать кнопку при неактивной эмуляции")
            return False
        if not button:
            self.__logger.error("Не указана кнопка мыши")
            return False
        return self._arduino._send_command("mouse", "press", button)

    def release(self, button: MouseButton) -> bool:
        if not self.__is_started:
            self.__logger.warning("Попытка отпустить кнопку при неактивной эмуляции")
            return False
        if not button:
            self.__logger.error("Не указана кнопка мыши")
            return False
        return self._arduino._send_command("mouse", "release", button)

    def click(self, button: MouseButton) -> bool:
        if not self.__is_started:
            self.__logger.warning("Попытка кликнуть кнопкой при неактивной эмуляции")
            return False
        if not button:
            self.__logger.error("Не указана кнопка мыши")
            return False
        return self._arduino._send_command("mouse", "click", button)

    def move_absolute(self, target_x: int, target_y: int, duration: float = 1.0, retry_level: int = 0) -> bool:
        if not self.__is_started:
            self.__logger.warning("Попытка перемещения при неактивной эмуляции")
            return False
        if duration <= 0:
            self.__logger.error("Некорректная длительность перемещения")
            return False

        self.__set_positions()
        target_x = max(0, min(int(target_x), self.__screen_width - 1))
        target_y = max(0, min(int(target_y), self.__screen_height - 1))

        if (target_x, target_y) == (self.__current_x, self.__current_y):
            return True

        start_x, start_y = self.__current_x, self.__current_y
        total_x, total_y = target_x - start_x, target_y - start_y
        steps = max(1, min(int(duration * 60), 300))
        step_delay = duration / steps
        max_deviation = 5.0

        for step in range(1, steps + 1):
            progress = step / steps
            eased_progress = progress

            expected_x = start_x + total_x * eased_progress
            expected_y = start_y + total_y * eased_progress

            rel_x = round(expected_x - self.__current_x)
            rel_y = round(expected_y - self.__current_y)

            if rel_x != 0 or rel_y != 0:
                if not self._arduino._send_command("mouse", "move", rel_x, rel_y):
                    self.__logger.error(f"Ошибка перемещения на шаге {step}")
                    return False

                self.__current_x += rel_x
                self.__current_y += rel_y

                actual_deviation = ((self.__current_x - expected_x) ** 2 +
                                    (self.__current_y - expected_y) ** 2) ** 0.5

                if actual_deviation > max_deviation:
                    if retry_level >= self.MAX_RETRY:
                        self.__logger.error("Слишком большое отклонение и превышен лимит коррекций")
                        return False
                    self.__logger.warning(f"Отклонение {actual_deviation:.1f}px, повтор с retry={retry_level + 1}")
                    return self.move_absolute(target_x, target_y, duration / 2, retry_level + 1)

            time.sleep(step_delay)

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
        if not self.__is_started:
            self.__logger.warning("Попытка перемещения при неактивной эмуляции")
            return False
        return self._arduino._send_command("mouse", "move", x, y)

    def get_position(self) -> Tuple[int, int]:
        return self.__current_x, self.__current_y
