from time import sleep

from src.arduino_hid_controller import HIDController
from src.arduino_hid_controller.constants import MOUSE_RIGHT, MOUSE_LEFT

with HIDController() as hid:
    print(f"Текущая позиция мыши: {hid.get_position()}")

    print('Ожидание 2 секунды...')
    sleep(2)

    print('Запуск эмуляции мыши')
    hid.mouse.start()

    print('Ожидание 2 секунды...')
    sleep(2)

    print('Перемещение мыши в координаты 500,300 и клик правой кнопкой')
    hid.mouse.move_absolute(500, 300, 1)
    hid.mouse.click(MOUSE_RIGHT)

    print('Ожидание 2 секунды...')
    sleep(2)

    print('Перемещение мыши в координаты 100,100 и клик левой кнопкой')
    hid.mouse.move_absolute(100, 100, 1)
    hid.mouse.click(MOUSE_LEFT)

    print('Ожидание 2 секунды...')
    sleep(2)

    print('Перемещение на 100 пикселей вправо/вниз и клик левой кнопкой')
    hid.mouse.move_relative(100, 100)
    hid.mouse.click()

    print('Ожидание 2 секунды...')
    sleep(2)

    print('Остановка эмуляции мыши')
    hid.mouse.stop()
