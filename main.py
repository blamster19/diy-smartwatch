from rp2040driver import *
from ui import *

lcd = LCD_1inch28()
lcd.set_bl_pwm(65535)
touch = Touch_CST816T(mode=0,LCD=lcd)
gyro = QMI8658()
battery = ADC(Pin(Vbat_Pin))

smartwatch = Ui(lcd, touch, gyro, battery)

running = True
try:
    while running:
        smartwatch.input()
        smartwatch.draw()

except KeyboardInterrupt:
    pass

lcd.fill(0)
lcd.show()
