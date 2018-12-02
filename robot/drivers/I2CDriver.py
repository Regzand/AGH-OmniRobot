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
                 signal_change_time: float
                 ):
        """
        Creates driver and initialises GPIO for the I2C communication
        :param data_channel: GPIO pin number dedicated to I2C SDA line
        :param clock_channel: GPIO pin number dedicated to I2C SCL line
        :param signal_change_time: time that it takes to change a signal
            on either of the I2C lines, every change is surrounded with
            sleep instructions (better be >= 1ms = 0.001s)
        """

        # initialize properties
        self._data_channel = data_channel
        self._clock_channel = clock_channel
        self._signal_change_time = signal_change_time


        # enable pull-up resistors on both I2C lines
        # clock is pulled up first to simulate STOP condition on the bus
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._clock_channel, GPIO.OUT)
        GPIO.setup(self._data_channel, GPIO.OUT)
        self._clock_down()
        self._data_down()

    def _signal_up(self, channel):
        """
        Sets given GPIO to '1' state.
        """
        sleep(self._signal_change_time / 2.0)
        GPIO.output(channel, 1)
        sleep(self._signal_change_time / 2.0)

    def _signal_down(self, channel):
        """ Sets given GPIO to '0' state. """
        sleep(self._signal_change_time / 2.0)
        GPIO.output(channel, 0)
        sleep(self._signal_change_time / 2.0)

    def _clock_up(self):
        """ Sets clock line to '1' state """
        self._signal_up(self._clock_channel)
        print("clock: 1")

    def _clock_down(self):
        """ Sets clock line to '0' state """
        self._signal_down(self._clock_channel)
        print("clock: 0")

    def _data_up(self):
        """ Sets data line to '1' state """
        self._signal_up(self._data_channel)
        print("data: 1")

    def _data_down(self):
        """ Sets data line to '0' state """
        self._signal_down(self._data_channel)
        print("data: 0")

    def _acquire_data(self):
        """
        Sets data line as GPIO output
        :return:
        """
        GPIO.setup(self._data_channel, GPIO.OUT)

    def _release_data(self):
        """
        Sets data line as GPIO output
        :return:
        """
        GPIO.setup(self._data_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def _set_data(self, value):
        """
        Sets given signal on data line.
        :param value: bit to send (0 or 1)
        """
        if value == 0:
            self._data_down()

        else:
            self._data_up()

    def _read_data(self):
        """
        Reads signal from data line.
        :return: logic state of data line
        """
        sleep(self._signal_change_time / 2.0)
        result = GPIO.input(self._data_channel)
        print("reading data: " + str(result))
        sleep(self._signal_change_time / 2.0)
        return result

    def _send_start_condition(self):
        """
        Sends start condition.
        Start: clock - low
        End: clock - low; data - low
        """
        self._data_up()
        self._clock_up()
        self._data_down()
        self._clock_down()

    def _send_stop_condition(self):
        """
        Sends stop condition.
        Start: clock - low
        End: clock - low; data - high
        """
        self._data_down()
        self._clock_up()
        self._data_up()
        self._clock_down()

    def _check_acknowledgement(self):
        """
        Checks the acknowledgement signal set by the slave device after the
        transmission of a single byte.
        Start: clock - low
        End: clock - low
        :return: acknowledgement bit value
        """
        # Sets data free
        sleep(self._signal_change_time / 2.0)

        self._clock_up()
        result = self._read_data()
        self._clock_down()

        return result

    def _send_acknowledgement(self):
        """
        Sends the acknowledgement signal to the slave device after the
        transmission of a single byte.
        Start: clock - low
        End: clock - low
        """
        self._data_down()
        self._clock_up()
        self._clock_down()

    def _send_byte_with_ack(self, byte):
        """
        Sends the byte through the I2C bus
        Start: clock - low
        End: clock - low
        :param byte: byte to send
        :return: acknowledgement received from the slave device
        """
        bin_rep = format(byte, '08b')
        for _, bit in zip(range(8), bin_rep):

            self._set_data(int(bit))
            self._clock_up()
            self._clock_down()

        self._release_data()
        result = self._check_acknowledgement()
        self._acquire_data()
        return result

    def _read_byte_with_ack(self):
        """
        Reads the byte through the I2C bus
        Start: clock - low
        End: clock - low
        :return: byte that has been read
        """

        # Sets data free
        sleep(self._signal_change_time)
        self._release_data()

        result = 0
        for i in range(8):

            self._clock_up()
            next_bit = self._read_data()
            self._clock_down()

            result = (result << 1) + next_bit

        self._acquire_data()
        self._send_acknowledgement()

        return result

    def cleanup(self):
        """ Cleans up GPIO configuration for both data nad clock channels """
        GPIO.cleanup(self._data_channel)
        GPIO.cleanup(self._clock_channel)


