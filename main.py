from rp2040driver import *
from ui import *
from oximeter import *
import _thread
from utime import ticks_ms, sleep

lcd = LCD_1inch28()
lcd.set_bl_pwm(65535)
touch = Touch_CST816T(mode=0,LCD=lcd)
gyro = QMI8658()
battery = ADC(Pin(Vbat_Pin))
sensor_sample_rate = 400
sensor_fifo_average = 8
actual_acquisition_rate = int(sensor_sample_rate / sensor_fifo_average)
hr_monitor = HeartRateMonitor(
        sample_rate=actual_acquisition_rate,
        window_size=int(actual_acquisition_rate * 3),
    )
oxi = Oximeter(hr_monitor, sensor_sample_rate, sensor_fifo_average)
bpm = 0
spo2 = 0

smartwatch = Ui(lcd, touch, gyro, battery)

# pulse oximeter thread
def core1():
    global bpm
    global spo2
    while True:
        bpm, spo2 = oxi.measure()
        print(str(bpm)+', '+str(spo2))

def core0():
    global bpm
    global spo2
    try:
        # UI thread
        while True:
            smartwatch.input()
            smartwatch.draw(bpm, spo2)

    except KeyboardInterrupt:
        pass

_thread.start_new_thread(core1, ())
core0()

lcd.fill(0)
lcd.show()