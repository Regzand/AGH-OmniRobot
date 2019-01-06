import math
from VL53L1X import VL53L1X


class VL53L1XDriver:

    def __init__(self, device_address, i2c_bus = 1):
        self._device_address = device_address
        self._tof = VL53L1X(i2c_bus=i2c_bus, i2c_address=device_address)
        self._ranging_mode = 3
        self._is_ranging = False
        self._tof.open()

    @property
    def ranging_mode(self):
        return self._ranging_mode

    @ranging_mode.setter
    def ranging_mode(self, new_ranging_mode):
        self._ranging_mode = new_ranging_mode
        if self._is_ranging:
            self.start()

    def start(self):
        self._is_ranging = True
        self._tof.start_ranging(self._ranging_mode)

    def stop(self):
        self._is_ranging = False
        self._tof.stop_ranging()

    @property
    def distance(self):
        if self._is_ranging:
            return self._tof.get_distance() / 10.

        return None
