from time import sleep

from src.arduino_hid_controller import HIDController, MouseButton

with HIDController() as hid:
    print(f"Текущая позиция мыши: {hid.mouse.get_position()}")

    print('Ожидание 2 секунды...')
    sleep(2)

    print('Запуск эмуляции мыши')
    hid.mouse.start()

    print('Ожидание 2 секунды...')
    sleep(2)

    print('Клик левой кнопкой')
    hid.mouse.click(MouseButton.LEFT)

    print('Ожидание 2 секунды...')
    sleep(2)

    print('Переходы по координатам...')
    points = [(100, 100), (100, 200), (200, 200), (200, 100), (100, 100)]
    for x, y in points:
        hid.mouse.move_absolute(x, y, duration=4)
        sleep(1)

    print('Ожидание 2 секунды...')
    sleep(2)

    print('Остановка эмуляции мыши')
    hid.mouse.stop()
