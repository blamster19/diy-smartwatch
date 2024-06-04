from rp2040driver import *
from ui import *

lcd = LCD_1inch28()
lcd.set_bl_pwm(65535)

touch=Touch_CST816T(mode=0,LCD=lcd)

smartwatch = Ui(lcd)

running = True
try:
    while running:
        smartwatch.draw()

except KeyboardInterrupt:
    pass

lcd.fill(0)
lcd.show()
