import math
from lsm303d import LSM303D


class Lsm303dDriver:

    def __init__(self, device_address):
        self._device_address = device_address
        self._lsm = LSM303D(device_address)

    @property
    def temperature(self):
        return self._lsm.temperature()

    @property
    def magnetic_field(self):
        return self._lsm.magnetometer()

    @property
    def magnetic_field_angle_xy(self):
        x, y, z = self.magnetic_field
        return math.atan2(y, x)

    @property
    def magnetic_field_angle_yz(self):
        x, y, z = self.magnetic_field
        return math.atan2(z, y)

    @property
    def magnetic_field_angle_xz(self):
        x, y, z = self.magnetic_field
        return math.atan2(z, x)

    @property
    def acceleration(self):
        return self._lsm.accelerometer()

    @property
    def acceleration_angle_xy(self):
        x, y, z = self.acceleration
        return math.atan2(y, x)

    @property
    def acceleration_angle_yz(self):
        x, y, z = self.acceleration
        return math.atan2(z, y)

    @property
    def acceleration_angle_xz(self):
        x, y, z = self.acceleration
        return math.atan2(z, x)
