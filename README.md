# DIY Smartwatch

This project is a firmware for my smartwatch based on [Waveshare RP2040 Touch LCD 1.28”](https://www.waveshare.com/rp2040-touch-lcd-1.28.htm) coupled with [MAX30102](https://www.analog.com/en/products/max30102.html).

# Flashing

Flash all files like a typical MicroPython program. The board is RP2040 based.

# Features

Program consists of three panels: date and time (RTC), pulse and saturation (pulse oximeter), and level bubble (accelerometer). You can switch between them by swiping up/down.

# TODO

- [ ] sleep
- [ ] better graphics
- [ ] smarter pulse oximeter data acquisition
- [ ] configurable date and time, UI, etc.
- [ ] Bluetooth
- [ ] WiFi
