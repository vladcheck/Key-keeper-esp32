from machine import Pin, PWM
from neopixel import NeoPixel
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
button_pins = [pin_in(23), pin_in(34)]
buzzer = Buzzer(17)
size_x = 2
size_y = 2
lights = NeoPixel(pin_in(13), 4)


def scan_matrix():
    button_pressed = False
    for i, pin in enumerate(button_pins):
        if pin.value() == 0:
            button_pressed = True
            x = i % size_x + 1
            y = i // size_y + 1
            lights[i] = (255, 255, 255)
            print(f"Button {x}:{y} pressed")
            buzzer.on()  # Включаем звук
            lights.write()
            pin.off()

    if not button_pressed:
        buzzer.off()  # Выключаем звук, если нет нажатых кнопок
        for i in range(len(lights)):
            lights[i] = (0, 0, 0)
        lights.write()


while True:
    scan_matrix()
    time.sleep(0.05)  # Уменьшили задержку для лучшей реакции
