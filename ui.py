from machine import RTC
import time

# UI class
#
# panel  -  currently displayed panel
# 			0 - date and time
# 			1 - water level
class Ui:
    def __init__(self, LCD):
        self.LCD = LCD
        self.panel = 0
        self.rtc = RTC()

    def draw(self):
        self.LCD.fill(0)
        
        # match panel
        if self.panel == 0 :
            self._draw_datetime_face()
        elif self.panel == 1:
            self._draw_water()
        
        self.LCD.show()
        
    def _draw_datetime_face(self)
        # draw time
        t = time.localtime()
        time_str = str(t[3])+':'+'{:02d}'.format(t[4])+':'+'{:02d}'.format(t[5])
        self.LCD.write_text(time_str, 25, 105, 3, 65535)
        # draw date
        date_str = str(t[0])+'-'+'{:02d}'.format(t[1])+'-'+'{:02d}'.format(t[2])
        self.LCD.write_text(date_str, 40, 140, 2, 65535)
        
    def _draw_water(self):
        pass