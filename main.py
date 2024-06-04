from rp2040driver import *
from ui import *

LCD = LCD_1inch28()
LCD.set_bl_pwm(65535)

Touch=Touch_CST816T(mode=0,LCD=LCD)

smartwatch = Ui(LCD)

running = True
try:
    while running:
        smartwatch.draw()

except KeyboardInterrupt:
    pass

LCD.fill(0)
LCD.show()
