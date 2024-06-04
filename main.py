from rp2040driver import *
from machine import RTC
import time

LCD = LCD_1inch28()
LCD.set_bl_pwm(65535)

Touch=Touch_CST816T(mode=0,LCD=LCD)
rtc = RTC()

def draw_ui(LCD):
    # draw time
    t = time.localtime()
    time_string = str(t[3])+':'+'{:02d}'.format(t[4])+':'+'{:02d}'.format(t[5])
    LCD.fill(0)
    LCD.write_text(time_string, 25, 105, 3, 65535)
    # draw date
    date_string = str(t[0])+'-'+'{:02d}'.format(t[1])+'-'+'{:02d}'.format(t[2])
    LCD.write_text(date_string, 40, 140, 2, 65535)
    LCD.show()

running = True
try:
    while running:

        draw_ui(LCD)


except KeyboardInterrupt:
    pass

LCD.fill(0)
LCD.show()
