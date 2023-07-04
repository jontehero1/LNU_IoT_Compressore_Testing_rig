from machine import Pin
import utime

class AngularSpeedSensor:
    def __init__(self, pin_number):
        self.pin = Pin(pin_number, Pin.IN)
        self.counter = 0
        self.prev_time = utime.ticks_ms()
        self.pin.irq(trigger=Pin.IRQ_RISING, handler=self._count)

    def _count(self, pin):
        self.counter += 1

    def read_angular_speed(self):
        curr_time = utime.ticks_ms()
        time_diff = utime.ticks_diff(curr_time, self.prev_time) / 1000

        if time_diff != 0:
            rpm = (self.counter * 60) / time_diff
            self.counter = 0
            self.prev_time = curr_time
            return rpm
        else:
            return 0
