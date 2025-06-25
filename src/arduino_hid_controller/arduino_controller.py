import serial
import serial.tools.list_ports
import time
import logging


class ArduinoController:
    """
    Класс управления Arduino.
    """

    # Известные VID/PID Arduino-совместимых устройств
    DEFAULT_VID_PID_LIST = [
        ("2341", "0043"),  # Arduino Uno
        ("2341", "8036"),  # Arduino Leonardo
        ("2341", "0001"),  # Arduino Uno (другой загрузчик)
        ("1A86", "7523"),  # CH340 USB-UART (часто в китайских Arduino)
        ("10C4", "EA60"),  # CP2102
        ("1A86", "55D4"),  # Некоторые китайские клоны
    ]

    def __init__(self, port: str = None, vid_pid_list=None, auto_reconnect: bool = True):
        """
        :param port: Указать порт вручную, если известно (например, 'COM5')
        :param vid_pid_list: Список допустимых VID/PID (список кортежей строк)
        :param auto_reconnect: Переподключение после отключения (True/False)
        """
        self.__user_port = port
        self.__auto_reconnect = auto_reconnect
        self.__vid_pid_list = vid_pid_list or self.DEFAULT_VID_PID_LIST
        self.__port = None
        self.__serial = None
        self.__logger = logging.getLogger(__name__)
        self.__open()

    @staticmethod
    def list_available_ports(verbose: bool = True):
        """
        Показать список всех доступных COM-портов
        """
        ports = serial.tools.list_ports.comports()
        for port in ports:
            info = f"{port.device} — {port.description} (VID={port.vid}, PID={port.pid})"
            if verbose:
                print(f"🔌 {info}")
        return ports

    def __find_arduino_port_by_vid_pid(self):
        """
        Поиск Arduino по VID/PID
        """
        ports = serial.tools.list_ports.comports()
        for port in ports:
            vid = f"{port.vid:04X}" if port.vid else None
            pid = f"{port.pid:04X}" if port.pid else None
            if vid and pid and (vid, pid) in self.__vid_pid_list:
                return port.device
        return None

    @staticmethod
    def suggest_ports(show_all: bool = False):
        """
        Показывает список COM-портов, пригодных для ручного выбора.
        :param show_all: если True — покажет все, иначе только похожие на Arduino
        """
        ports = serial.tools.list_ports.comports()
        if not ports:
            print("❌ Порты не найдены.")
            return

        print("📋 Доступные COM-порты:")
        for port in ports:
            description = port.description or "Нет описания"
            vid = f"{port.vid:04X}" if port.vid else "--"
            pid = f"{port.pid:04X}" if port.pid else "--"
            match = any(
                (f"{port.vid:04X}", f"{port.pid:04X}") == known
                for known in ArduinoController.DEFAULT_VID_PID_LIST
            )
            if show_all or match or any(x in description for x in ["Arduino", "Serial", "CH340"]):
                print(f"🔌 {port.device}: {description} (VID={vid}, PID={pid})")

    def __find_arduino_port_by_description(self):
        """
        Резервный способ: поиск по описанию
        """
        arduino_identifiers = [
            "Arduino", "CH340", "USB Serial Device", "USB2.0-Serial",
            "Leonardo", "Pro Micro", "CDC", "Composite", "ttyACM", "ttyUSB"
        ]
        ports = serial.tools.list_ports.comports()
        for port in ports:
            desc = port.description or ""
            if any(identifier.lower() in desc.lower() for identifier in arduino_identifiers):
                return port.device
        return None

    def __find_arduino_port(self):
        """
        Пытается найти Arduino автоматически
        """
        port = self.__find_arduino_port_by_vid_pid()
        if port:
            self.__logger.info(f"✅ Найден Arduino по VID/PID: {port}")
            return port

        port = self.__find_arduino_port_by_description()
        if port:
            self.__logger.info(f"✅ Найден Arduino по описанию: {port}")
            return port

        return None

    def __open(self):
        """Подключение к Arduino"""
        if self.__serial and self.__serial.is_open:
            return

        self.__port = self.__user_port or self.__find_arduino_port()

        if not self.__port:
            self.suggest_ports(show_all=True)
            raise RuntimeError("❌ Arduino не найден. Укажите порт вручную или проверьте подключение.")

        for attempt in range(3):
            try:
                self.__serial = serial.Serial(self.__port, baudrate=9600, timeout=1)
                time.sleep(2)
                if self.__serial.is_open:
                    self.__logger.info(f"✅ Подключено к Arduino на порту {self.__port}")
                    return
            except serial.SerialException as e:
                self.__logger.warning(f"⚠️ Попытка {attempt + 1}: {e}")
                time.sleep(1)

        self.suggest_ports()
        raise RuntimeError(
            f"❌ Не удалось подключиться к {self.__port}. "
            f"Порт может быть занят или Arduino не готов. "
            f"Укажите другой порт вручную через `ArduinoController(port='COMX')`."
        )

    @property
    def __is_connected(self):
        return self.__serial is not None and self.__serial.is_open

    def __close(self):
        if self.__is_connected:
            try:
                self.__serial.close()
                self.__logger.info("🔌 Соединение с Arduino закрыто")
            except serial.SerialException as e:
                self.__logger.error(f"Ошибка при закрытии соединения: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close()

    def _send_command(self, device: str, action: str, *args) -> bool:
        """
        Отправка команды на Arduino и получение ответа
        """
        command = f"{device}|{action}|"
        if args:
            command += "|".join(str(arg) for arg in args)

        if not self.__is_connected:
            self.__logger.warning("⚠️ Arduino отключён.")
            if self.__auto_reconnect:
                self.__logger.info("🔄 Пытаемся автоматически переподключиться...")
                for attempt in range(10):
                    try:
                        self.__open()
                        self.__logger.info("✅ Переподключено к Arduino.")
                        break
                    except Exception as e:
                        self.__logger.debug(f"⏳ Попытка {attempt + 1}: {e}")
                        time.sleep(3)
                else:
                    self.__logger.error("❌ Не удалось переподключиться к Arduino.")
                    return False
            else:
                return False

        try:
            self.__serial.write(f"{command}\n".encode())
            response = self.__serial.readline().decode().strip()
            return response == "True"
        except serial.SerialException as e:
            self.__logger.error(f"❌ Ошибка связи: {e}")
            self.__serial = None  # Отметим как отключённое
            return False

