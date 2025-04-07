import serial
import serial.tools.list_ports
import time
import logging


class ArduinoController:
    """Базовый класс для управления Arduino через последовательный порт"""

    def __init__(self):
        """
        Инициализация контроллера
        """
        self.__port = None
        self.__serial = None
        self.__logger = logging.getLogger(__name__)
        self.__open()

    @staticmethod
    def __find_arduino_port():
        """
        Определяет порт Arduino.
        """
        ports = serial.tools.list_ports.comports()
        arduino_identifiers = ["Arduino", "CH340", "USB Serial Device", "USB2.0-Serial"]
        for port in ports:
            if any(identifier in port.description for identifier in arduino_identifiers):
                return port.device
        return None

    def __open(self):
        """Открытие соединения"""
        if self.__serial is None or not self.__serial.is_open:
            self.__port = self.__find_arduino_port()
            if not self.__port:
                raise RuntimeError("Arduino не найден. Проверьте подключение.")
            try:
                self.__serial = serial.Serial(self.__port, baudrate=9600, timeout=1)
                time.sleep(2)  # Даем время для инициализации
                self.__logger.info(f"Подключено к Arduino на порту {self.__port}")
            except serial.SerialException as e:
                self.__logger.error(f"Ошибка подключения: {e}")
                raise RuntimeError(f"Не удалось подключиться к Arduino: {e}")

    @property
    def __is_connected(self):
        """Проверка активного соединения"""
        return self.__serial is not None and self.__serial.is_open

    def __close(self):
        """Закрытие соединения"""
        if self.__is_connected:
            try:
                self.__serial.close()
                self.__logger.info("Соединение с Arduino закрыто")
            except serial.SerialException as e:
                self.__logger.error(f"Ошибка при закрытии соединения: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close()

    def _send_command(self, device: str, action: str, *args) -> bool:
        """
        Отправка команды на Arduino и получение ответа

        Аргументы:
            device: Устройство ('keyboard' или 'mouse')
            action: Действие (например, 'press', 'move' и т.д.)
            *args: Аргументы команды

        Возвращает:
            bool: True если команда выполнена успешно, False в противном случае
        """
        if not self.__is_connected:
            self.__logger.warning("Попытка отправить команду без соединения")
            return False

        command = f"{device}|{action}"
        if args:
            command += "|" + "|".join(str(arg) for arg in args)

        try:
            self.__serial.write(f"{command}\n".encode())
            response = self.__serial.readline().decode().strip()
            return response == "True"
        except serial.SerialException as e:
            self.__logger.error(f"Ошибка связи: {e}")
            return False
