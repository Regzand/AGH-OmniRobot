import RPi.GPIO as GPIO


class MotorDriver:
    """
    Driver for servo motor that allows for controlling motor speed with servo related corrections.
    """

    def __init__(self,
                 channel: int,
                 speed: float = 0,
                 frequency: float = 50,
                 min_duty_cycle: float = 5,
                 max_duty_cycle: float = 10,
                 forward_scale: float = 1,
                 backward_scale: float = 1,
                 offset: float = 0,
                 epsilon: float = 0.15
                 ):
        """
        Creates driver and initialise GPIO for the motor
        :param channel: Raspberry Pi channel number to connect to
        :param speed: initial speed of motor
        :param frequency: frequency of PWM signal cycle
        :param min_duty_cycle: minimal duty cycle of the motor, corresponding to speed = -1
        :param max_duty_cycle: maximal duty cycle of the motor, corresponding to speed = 1
        :param forward_scale: scale between speed and duty cycle for speeds in range (0, 1]
        :param backward_scale: scale between speed and duty cycle for speeds in range [-1, 0)
        :param offset: offset of neutral duty cycle, corresponding to speed = 0
        :param epsilon: epsilon of speed below which the motor will be stopped
        """
        self._channel = channel

        # initialize properties
        self._speed = speed
        self._frequency = frequency
        self._min_duty_cycle = min_duty_cycle
        self._max_duty_cycle = max_duty_cycle
        self._forward_scale = forward_scale
        self._backward_scale = backward_scale
        self._offset = offset
        self._epsilon = epsilon

        # setup GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(channel, GPIO.OUT)
        self._pwm = GPIO.PWM(channel, frequency)
        self._pwm.start(0)

        self._update_duty_cycle()

    def cleanup(self):
        """ Stops the motor and cleans up GPIO configuration for motor channel """
        self._pwm.stop()
        GPIO.cleanup(self._channel)

    def _update_duty_cycle(self):
        """ Updates PWN duty cycle based on driver configuration. If speed is below epsilon stops motor. """
        if abs(self.speed) <= self.epsilon:
            self._pwm.ChangeDutyCycle(0)
            return

        # calculate speed
        speed = self.speed
        speed *= self.forward_scale if speed > 0 else self.backward_scale
        speed = max(min(speed, 1), -1)

        # calculate neutral duty cycle
        duty_cycle = (self.max_duty_cycle + self.min_duty_cycle) / 2
        duty_cycle += self.offset

        # calculate duty cycle
        duty_cycle += speed * (self.max_duty_cycle - self.min_duty_cycle) / 2

        # update PWM
        self._pwm.ChangeDutyCycle(duty_cycle)

    @property
    def speed(self) -> float:
        """ Gets or sets motor speed. Speed has to be in range of [-1, 1]. Updates PWM. """
        return self._speed

    @speed.setter
    def speed(self, speed: float):
        self._speed = max(min(speed, 1), -1)
        self._update_duty_cycle()

    @property
    def frequency(self) -> float:
        """ Gets or sets frequency of PWM signal cycle. Updates PWM. """
        return self._frequency

    @frequency.setter
    def frequency(self, frequency: float):
        self._frequency = frequency
        self._pwm.ChangeFrequency(self.frequency)

    @property
    def min_duty_cycle(self) -> float:
        """ Gets or sets minimal duty cycle of the motor. Updates PWM. """
        return self._min_duty_cycle

    @min_duty_cycle.setter
    def min_duty_cycle(self, min_duty_cycle: float):
        self._min_duty_cycle = min_duty_cycle
        self._update_duty_cycle()

    @property
    def max_duty_cycle(self) -> float:
        """ Gets or sets maximal duty cycle of the motor. Updates PWM. """
        return self._max_duty_cycle

    @max_duty_cycle.setter
    def max_duty_cycle(self, max_duty_cycle: float):
        self._max_duty_cycle = max_duty_cycle
        self._update_duty_cycle()

    @property
    def forward_scale(self) -> float:
        """ Gets or sets scale between speed and duty cycle for speeds in range (0, 1]. Updates PWM. """
        return self._forward_scale

    @forward_scale.setter
    def forward_scale(self, forward_scale: float):
        self._forward_scale = forward_scale
        self._update_duty_cycle()

    @property
    def backward_scale(self) -> float:
        """ Gets or sets scale between speed and duty cycle for speeds in range [-1, 0). Updates PWM. """
        return self._backward_scale

    @backward_scale.setter
    def backward_scale(self, backward_scale: float):
        self._backward_scale = backward_scale
        self._update_duty_cycle()

    @property
    def offset(self) -> float:
        """ Gets or sets offset of neutral duty cycle. Updates PWM. """
        return self._offset

    @offset.setter
    def offset(self, offset: float):
        self._offset = offset
        self._update_duty_cycle()

    @property
    def epsilon(self) -> float:
        """ Gets or sets epsilon of speed below which the motor will be stopped. Updates PWM. """
        return self._epsilon

    @epsilon.setter
    def epsilon(self, epsilon: float):
        self._epsilon = epsilon
        self._update_duty_cycle()
