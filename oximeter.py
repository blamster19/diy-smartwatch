# based on library's example
# https://github.com/n-elia/MAX30102-MicroPython-driver

from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM
from machine import SoftI2C, Pin
from utime import ticks_ms, ticks_diff


class Oximeter:
    def __init__(self, hr_monitor, sensor_sample_rate, sensor_fifo_average):
        i2c = SoftI2C(sda=Pin(26),
                      scl=Pin(27),
                      freq=400000)
        max30105 = MAX30102(i2c=i2c)
        # sanity check
        if max30105.i2c_address not in i2c.scan():
            print("Sensor not found.")
            return
        elif not (max30105.check_part_id()):
            print("I2C device ID not corresponding to MAX30102 or MAX30105.")
            return
        else:
            print("Sensor connected and recognized.")
        # setup
        print("Setting up sensor with default configuration.", '\n')
        max30105.setup_sensor()
        max30105.set_sample_rate(sensor_sample_rate)
        max30105.set_fifo_average(sensor_fifo_average)
        max30105.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)
        print("Reading temperature in °C.", '\n')
        print(max30105.read_temperature())
        
        self.sensor = max30105
        self.actual_acquisition_rate = int(sensor_sample_rate / sensor_fifo_average)
        self.hr_compute_interval = 2
        self.hr_monitor = hr_monitor
        
    def measure(self):
        ref_time = ticks_ms()
        heart_rate = 0
        while True:
            self.sensor.check()
            if self.sensor.available():
                red_reading = self.sensor.pop_red_from_storage()
                ir_reading = self.sensor.pop_ir_from_storage()
                self.hr_monitor.add_sample(ir_reading, red_reading)
            if ticks_diff(ticks_ms(), ref_time) / 1000 > self.hr_compute_interval:
    #         if True:
                heart_rate = self.hr_monitor.calculate_heart_rate() 
                ref_time = ticks_ms()
                break
        return heart_rate
        
class HeartRateMonitor:
    """A simple heart rate monitor that uses a moving window to smooth the signal and find peaks."""

    def __init__(self, sample_rate=100, window_size=10, smoothing_window=5):
        self.sample_rate = sample_rate
        self.window_size = window_size
        self.smoothing_window = smoothing_window
        self.ir_samples = []
        self.red_samples = []
        self.timestamps = []
        self.filtered_ir_samples = []
        self.filtered_red_samples = []

    def add_sample(self, ir_sample, red_sample):
        """Add a new sample to the monitor."""
        timestamp = ticks_ms()
        self.ir_samples.append(ir_sample)
        self.red_samples.append(red_sample)
        self.timestamps.append(timestamp)

        # Apply smoothing
        if len(self.ir_samples) >= self.smoothing_window:
            smoothed_ir_sample = (
                sum(self.ir_samples[-self.smoothing_window :]) / self.smoothing_window
            )
            self.filtered_ir_samples.append(smoothed_ir_sample)
        else:
            self.filtered_ir_samples.append(ir_sample)
        if len(self.red_samples) >= self.smoothing_window:
            smoothed_red_sample = (
                sum(self.red_samples[-self.smoothing_window :]) / self.smoothing_window
            )
            self.filtered_red_samples.append(smoothed_red_sample)
        else:
            self.filtered_red_samples.append(red_sample)

        # Maintain the size of samples and timestamps
        if len(self.ir_samples) > self.window_size or len(self.red_samples) > self.window_size:
            self.ir_samples.pop(0)
            self.timestamps.pop(0)
            self.filtered_ir_samples.pop(0)
            self.red_samples.pop(0)
            self.filtered_red_samples.pop(0)


    def find_ir_peaks(self):
        """Find peaks in the filtered ir_samples."""
        peaks = []

        if len(self.filtered_ir_samples) < 2:  # Need at least three samples to find a peak
            return peaks

        # Calculate dynamic threshold based on the min and max of the recent window of filtered samples
        recent_ir_samples = self.filtered_ir_samples[-self.window_size :]
        min_val = min(recent_ir_samples)
        max_val = max(recent_ir_samples)
        threshold = (
            min_val + (max_val - min_val) * 0.5
        )  # 50% between min and max as a threshold

        for i in range(1, len(self.filtered_ir_samples) - 1):
            if (
                self.filtered_ir_samples[i] > threshold
                and self.filtered_ir_samples[i - 1] < self.filtered_ir_samples[i]
                and self.filtered_ir_samples[i] > self.filtered_ir_samples[i + 1]
            ):
                peak_time = self.timestamps[i]
                peaks.append((peak_time, self.filtered_ir_samples[i]))

        return peaks
    
    def find_red_peaks(self):
        """Find peaks in the filtered ir_samples."""
        peaks = []

        if len(self.filtered_red_samples) < 2:  # Need at least three samples to find a peak
            return peaks

        # Calculate dynamic threshold based on the min and max of the recent window of filtered samples
        recent_red_samples = self.filtered_red_samples[-self.window_size :]
        min_val = min(recent_red_samples)
        max_val = max(recent_red_samples)
        threshold = (
            min_val + (max_val - min_val) * 0.5
        )  # 50% between min and max as a threshold

        for i in range(1, len(self.filtered_red_samples) - 1):
            if (
                self.filtered_red_samples[i] > threshold
                and self.filtered_red_samples[i - 1] < self.filtered_red_samples[i]
                and self.filtered_red_samples[i] > self.filtered_red_samples[i + 1]
            ):
                peak_time = self.timestamps[i]
                peaks.append((peak_time, self.filtered_red_samples[i]))

        return peaks

    def calculate_heart_rate(self):
        """Calculate the heart rate in beats per minute (BPM)."""
        
        ir_peaks = self.find_ir_peaks()
        red_peaks = self.find_red_peaks()


        if len(ir_peaks) < 5:
            return None, None  # Not enough peaks to calculate heart rate
#         if len(red_peaks) < 5:
#             return None, None

        # Calculate the average interval between peaks in milliseconds
        intervals = []
        for i in range(1, len(ir_peaks)):
            interval = ticks_diff(ir_peaks[i][0], ir_peaks[i - 1][0])
            intervals.append(interval)

        average_interval = sum(intervals) / len(intervals)

        # Convert intervals to heart rate in beats per minute (BPM)
        heart_rate = (
            60000 / average_interval
        )  # 60 seconds per minute * 1000 ms per second
        
        # SpO2
#         ratios = [red_peaks[i][0] / ir_peaks[i][0] for i in range(min(len(red_peaks), len(ir_peaks)))]
#         spo2 = 100 - 5 * sum(ratios) / len(ratios)
        R = sum(red_peaks[:][0]) / sum(ir_peaks[:][0]) * len(ir_peaks[:][0]) / len(red_peaks[:][0])
        spo2 = 100 - 5 * R

        return heart_rate, spo2