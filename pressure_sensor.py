import machine
import time
from machine import Pin
DEFAULT_ADDRESS = 0x18
MAXIMUM_Pa = 172368.932
MINIMUM_Pa = 0

OUTPUT_MAX = 0xE66666
OUTPUT_MIN = 0x19999A


class SparkFunMicroPressure:
    def __init__(self):
        self._address = DEFAULT_ADDRESS
        self._min_Pa = MINIMUM_Pa
        self._max_Pa = MAXIMUM_Pa
        self._i2c = machine.I2C(0, scl=Pin(21), sda=Pin(20))
        time.sleep(1)

    def read_status(self):
        self._i2c.writeto(self._address, bytes([0]))
        status = self._i2c.readfrom(self._address, 1)[0]
        return status

    def read_pressure(self):
        # Read pressure data
        self._i2c.writeto(self._address, bytes([0xAA, 0x00, 0x00]))
        time.sleep_ms(5)
        
        self._i2c.writeto(self._address, bytes([1]))
        data = self._i2c.readfrom(self._address, 4)
        
        pressure_data = data[1:]
        pressure = int.from_bytes(pressure_data, "big", False)
        
        # Scale pressure to the desired unit
        Pa = (((pressure - OUTPUT_MIN) * (self._max_Pa - self._min_Pa)) / (OUTPUT_MAX - OUTPUT_MIN)) + self._min_Pa

        return Pa
