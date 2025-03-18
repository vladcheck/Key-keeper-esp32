from machine import Pin, PWM
import time


def pin_in(number):
    return Pin(number, Pin.IN, Pin.PULL_DOWN)


class Buzzer:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin))
        self.active = False

    def on(self, frequency=440):
        if not self.active:
            self.pwm.freq(frequency)
            self.pwm.duty(512)
            self.active = True

    def off(self):
        if self.active:
            self.pwm.duty(0)
            self.active = False


# Инициализация пинов
button_pins = [pin_in(16), pin_in(17), pin_in(19), pin_in(18)]
buzzer = Buzzer(15)
size_x = 2
size_y = 2


def scan_matrix():
    button_pressed = False
    for i, pin in enumerate(button_pins):
        if pin.value() == 1:
            button_pressed = True
            x = i % size_x + 1
            y = i // size_y + 1
            print(f"Button {x}:{y} pressed")
            buzzer.on()  # Включаем звук

            pin.off()

    if not button_pressed:
        buzzer.off()  # Выключаем звук, если нет нажатых кнопок


while True:
    scan_matrix()
    time.sleep(0.05)  # Уменьшили задержку для лучшей реакции
