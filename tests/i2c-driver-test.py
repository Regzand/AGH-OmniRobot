import math

from robot.drivers.I2CDriver import I2CDriver

driver = I2CDriver(data_channel=3, clock_channel=5, clock_pulse_time=0.005)

driver._send_start_condition()
#driver._send_raw_byte(0b00111101)
driver._send_raw_byte(0b00011101)
print(driver._check_acknowledgement())
