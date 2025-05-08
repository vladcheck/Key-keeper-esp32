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
button_rows = [pin_in(12), pin_in(13)]
button_columns = [pin_in(26), pin_in(27)]
buzzer = Buzzer(23)
lights = NeoPixel(Pin(32, Pin.OUT), 4)
size_x = 2
size_y = 2

def scan_matrix():
    button_pressed = False
    for row_num, row_pin in enumerate(button_rows):
        row_pin.on()

        for col_num, col_pin in enumerate(button_columns):
            if col_pin.value() == 0:
                button_pressed = True
                lights[(col_num+row_num+1)] = (255, 255, 255)
                lights.write()
                buzzer.on()
                print(f"Button {row_num}:{col_num} pressed")

        row_pin.off()

    if not button_pressed:
        buzzer.off()  # Выключаем звук, если нет нажатых кнопок
        for i in range(len(lights)):
            lights[i] = (0, 0, 0)
        lights.write()

buzzer.off()
while True:
    scan_matrix()
    time.sleep(0.05)  # Уменьшили задержку для лучшей реакции
