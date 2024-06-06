from machine import RTC
import time

def color(r, g, b):
    return (((g&0b00011100)<<3) +((b&0b11111000)>>3)<<8) + (r&0b11111000)+((g&0b11100000)>>5)
# UI class
#
# panel  -  currently displayed panel
# 			0 - date and time
# 			1 - pulse oximeter

class Ui:
    def __init__(self, lcd, touch, gyro, battery):
        self.lcd = lcd
        self.touch = touch
        self.gyro = gyro
        self.battery = battery
        self.panel = 0
        self.rtc = RTC()
        self.max_panel = 1

    def draw(self):
        self.lcd.fill(0)
        
        # match panel
        if self.panel == 0 :
            self._draw_datetime_face()
        elif self.panel == 1:
            self._draw_bpm(69, 90)
        
        self.lcd.show()

    def input(self):
        # swipe up
        if self.touch.Gestures == 0x01:
            self.touch.Gestures = 0
            self.panel += 1
            if self.panel >= self.max_panel:
                self.panel = self.max_panel

        # swipe down
        elif self.touch.Gestures == 0x02:
            self.touch.Gestures = 0
            self.panel -= 1
            if self.panel < 1:
                self.panel = 0
        time.sleep(0.1)
        
    def _draw_datetime_face(self):
        # draw time
        t = time.localtime()
        time_str = '{:02d}'.format(t[3])+':'+'{:02d}'.format(t[4])+':'+'{:02d}'.format(t[5])
        self.lcd.write_text(time_str, 25, 105, 3, 65535)
        # draw date
        date_str = str(t[0])+'-'+'{:02d}'.format(t[1])+'-'+'{:02d}'.format(t[2])
        self.lcd.write_text(date_str, 40, 140, 2, 65535)
        self._draw_down_arrow()

    def _draw_bpm(self, bpm, spo2):
        # draw pulse
        self.lcd.write_text('bpm', 30, 60, 2, color(255, 255, 255))
        self.lcd.write_text(str(bpm), 40, 90, 7, color(255, 255, 255))
        self.lcd.write_text('SpO2', 160, 160, 1, color(255, 255, 255))
        self.lcd.write_text(str(spo2)+'%', 100, 170, 4, color(114, 226, 59))
        self._draw_up_arrow()

    def _draw_up_arrow(self):
        x = 0
        for y in range(10,20):
            x = x + 1
            self.lcd.hline(120-x, y,3,color(0,255,255))
            self.lcd.hline(117+x, y,3,color(0,255,255))

    def _draw_down_arrow(self):
        x = 0
        for y in range(209,199, -1):
            x = x + 1
            self.lcd.hline(120-x, y,3,color(0,255,255))
            self.lcd.hline(117+x, y,3,color(0,255,255))