from time import sleep

from src.arduino_hid_controller import HIDController, KeyboardKey

with HIDController() as hid:
    print('Запуск эмуляции клавиатуры')
    hid.keyboard.start()

    print('Ожидание 2 секунды...')
    sleep(2)

    print('Вызов клавиши А')
    hid.keyboard.press('A')
    sleep(0.15)
    hid.keyboard.release('A')

    print('Ожидание 2 секунды...')
    sleep(2)

    print('Вызов клавиши F12')
    hid.keyboard.press(KeyboardKey.F12)
    sleep(0.15)
    hid.keyboard.release(KeyboardKey.F12)

    print('Ожидание 2 секунды...')
    sleep(2)

    print('Вызов комбинации CTRL+ALT+DELETE')
    hid.keyboard.press(KeyboardKey.LEFT_CTRL)
    sleep(0.01)
    hid.keyboard.press(KeyboardKey.LEFT_ALT)
    sleep(0.01)
    hid.keyboard.press(KeyboardKey.DELETE)
    sleep(0.05)
    hid.keyboard.release_all()

    print('Вызов комбинации CTRL+ALT+DELETE через key combo')
    hid.keyboard.key_combo([KeyboardKey.LEFT_CTRL, KeyboardKey.LEFT_ALT, KeyboardKey.DELETE])

    print('Ожидание 2 секунды...')
    sleep(2)

    print('Остановка эмуляции клавиатуры')
    hid.keyboard.stop()
