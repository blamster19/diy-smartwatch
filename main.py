from rp2040driver import *

LCD = LCD_1inch28()
LCD.set_bl_pwm(65535)

Touch=Touch_CST816T(mode=0,LCD=LCD)