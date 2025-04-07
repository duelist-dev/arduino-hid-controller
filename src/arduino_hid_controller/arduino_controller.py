import serial
import serial.tools.list_ports
import time


class ArduinoController:
    """Базовый класс для управления Arduino через последовательный порт"""

    def __init__(self):
        """
        Инициализация контроллера
        """
        self.port = None
        self.serial = None
        self.open()

    @staticmethod
    def _find_arduino_port():
        """
        Определяет порт Arduino.
        """
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "Arduino" in port.description or "CH340" in port.description:
                return port.device
        return None

    def open(self):
        """Открытие соединения"""
        if self.serial is None or not self.serial.is_open:
            self.port = self._find_arduino_port()
            if not self.port:
                raise RuntimeError("Arduino не найден. Проверьте подключение.")
            self.serial = serial.Serial(self.port, baudrate=9600)
            time.sleep(2)

    def close(self):
        """Закрытие соединения"""
        if self.serial.is_open:
            self.serial.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

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
        command = f"{device}|{action}"
        if args:
            command += "|" + "|".join(str(arg) for arg in args)

        self.serial.write(f"{command}\n".encode())
        response = self.serial.readline().decode().strip()
        return response == "True"
