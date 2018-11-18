from __future__ import division
from time import sleep
import RPi.GPIO as GPIO


class I2CDriver:
    """
    Driver for transferring data between raspberry pi and sensors using
    pi's GIPO to simulate I2C bus.
    """

    def __init__(self,
                 data_channel: int,
                 clock_channel: int,
                 clock_pulse_time: float
                 ):
        """
        Creates driver and initialises GPIO for the I2C communication
        :param data_channel: GPIO pin number dedicated to I2C SDA line
        :param clock_channel: GPIO pin number dedicated to I2C SCL line
        :param clock_pulse_time: time of a single clock pulse in seconds
            (better be >= 1ms = 0.001s)
        """

        # initialize properties
        self._data_channel = data_channel
        self._clock_channel = clock_channel
        self._clock_pulse_time = clock_pulse_time


        # enable pull-up resistors on both I2C lines
        # clock is pulled up first to simulate STOP condition on the bus
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(clock_channel, GPIO.OUT)
        sleep(clock_pulse_time / 2.0)
        GPIO.setup(data_channel, GPIO.OUT)
        GPIO.add_event_detect(clock_channel, GPIO.FALLING,
                              callback=(lambda x: print('clock down')))
        GPIO.add_event_detect(clock_channel, GPIO.RISING,
                              callback=(lambda x: print('clock up')))
        GPIO.add_event_detect(data_channel, GPIO.FALLING,
                              callback=(lambda x: print('data down')))
        GPIO.add_event_detect(data_channel, GPIO.RISING,
                              callback=(lambda x: print('data down')))

    def _send_start_condition(self):
        """
        Sets both clock and data to high, then pulls data low.
        """

        sleep(self._clock_pulse_time)

        GPIO.setup(self._clock_channel, GPIO.OUT)
        GPIO.output(self._clock_channel, 1)
        sleep(self._clock_pulse_time / 2.0)
        GPIO.setup(self._data_channel, GPIO.OUT)
        GPIO.output(self._data_channel, 1)
        sleep(self._clock_pulse_time / 2.0)
        GPIO.output(self._data_channel, 0)

        sleep(self._clock_pulse_time)

    def _send_stop_condition(self):
        """
        Sets both clock to high and data to low, then pulls data up.
        """

        sleep(self._clock_pulse_time)

        GPIO.setup(self._clock_channel, GPIO.OUT)
        GPIO.output(self._clock_channel, 1)
        sleep(self._clock_pulse_time / 2.0)
        GPIO.setup(self._data_channel, GPIO.OUT)
        GPIO.output(self._data_channel, 0)
        sleep(self._clock_pulse_time / 2.0)
        GPIO.output(self._data_channel, 1)

        sleep(self._clock_pulse_time)

    def _check_acknowledgement(self):
        """
        Checks the acknowledgement signal set by the slave device after the
        transmission of a single byte.
        :return: acknowledgement bit value
        """

        sleep(self._clock_pulse_time)

        # Pulls clock down
        GPIO.setup(self._clock_channel, GPIO.OUT)
        GPIO.output(self._clock_channel, 0)
        sleep(self._clock_pulse_time / 2.0)

        # Sets data free
        GPIO.setup(self._data_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        sleep(self._clock_pulse_time / 2.0)

        # Pulls clock up
        GPIO.output(self._clock_channel, 1)
        sleep(self._clock_pulse_time / 2.0)

        # Reads the signal on data line
        result = GPIO.input(self._data_channel)
        sleep(self._clock_pulse_time / 2.0)

        # Pulls clock down to terminate acknowledgement pulse
        GPIO.output(self._clock_channel, 0)
        sleep(self._clock_pulse_time)

        # Pulls clock up terminating acknowledgement process
        sleep(self._clock_pulse_time / 2.0)
        GPIO.output(self._clock_channel, 1)

        sleep(self._clock_pulse_time)

        return result

    def _send_acknowledgement(self):
        """
        Sends the acknowledgement signal to the slave device after the
        transmission of a single byte.
        """

        sleep(self._clock_pulse_time)

        # Pulls clock down
        GPIO.setup(self._clock_channel, GPIO.OUT)
        GPIO.output(self._clock_channel, 0)
        sleep(self._clock_pulse_time / 2.0)

        # Pulls data down
        GPIO.setup(self._data_channel, GPIO.OUT)
        GPIO.output(self._data_channel, 0)
        sleep(self._clock_pulse_time / 2.0)

        # Pulls clock up
        GPIO.output(self._clock_channel, 1)
        sleep(self._clock_pulse_time)

        # Pulls clock down
        GPIO.output(self._clock_channel, 0)
        sleep(self._clock_pulse_time)

        # Pulls clock up again terminating acknowledgement process
        GPIO.output(self._clock_channel, 1)

        sleep(self._clock_pulse_time)

    def _send_raw_byte(self, byte):
        """
        Sends the byte through the I2C bus
        :param byte: byte to send
        :return: acknowledgement received from the slave device
        """

        sleep(self._clock_pulse_time)
        GPIO.setup(self._clock_channel, GPIO.OUT)
        GPIO.setup(self._data_channel, GPIO.OUT)

        bin_rep = format(byte, '08b')
        for i, bit in zip(range(8), bin_rep):

            # Pulls clock down
            GPIO.output(self._clock_channel, 0)
            sleep(self._clock_pulse_time / 2.0)

            # Sets data line
            GPIO.output(self._data_channel, int(bit))
            sleep(self._clock_pulse_time / 2.0)

            # Pulls clock up
            GPIO.output(self._clock_channel, 1)
            sleep(self._clock_pulse_time)

        return self._check_acknowledgement()

    def _read_raw_byte(self):
        """
        Reads the byte through the I2C bus
        :return: byte that has been read
        """

        sleep(self._clock_pulse_time)
        GPIO.setup(self._clock_channel, GPIO.OUT)
        GPIO.setup(self._data_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        result = 0
        for i in range(8):

            # Pulls clock down
            GPIO.output(self._clock_channel, 0)
            sleep(self._clock_pulse_time)

            # Pulls clock up
            GPIO.output(self._clock_channel, 1)
            sleep(self._clock_pulse_time / 2.0)

            # Reads data line
            next_bit = GPIO.input(self._data_channel)
            result = (result << 1) + next_bit
            sleep(self._clock_pulse_time / 2.0)

        self._send_acknowledgement()

        return result

    def cleanup(self):
        """ Cleans up GPIO configuration for both data nad clock channels """
        GPIO.cleanup(self._data_channel)
        GPIO.cleanup(self._clock_channel)


