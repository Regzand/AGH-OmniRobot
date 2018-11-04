import math

from MotorDriver import MotorDriver


class MovementController:
    """
    Class responsible for controlling the movement of the robot by properly adjusting the speed
    of each one of the three motors.

    The controller assumes that the motors ale set up in a way, that each wheel creates one vertex
    of an equilateral triangle. The naming convention for each motor is "motorA", where "A"
    denotes the angle of rotation relatively to some arbitrary value.
    """

    def __init__(self,
                 motor000: MotorDriver,
                 motor120: MotorDriver,
                 motor240: MotorDriver
                 ):
        """
        Creates the controller of three already calibrated motors.
        :param motor000: motor aligned with the 0 direction
        :param motor120: motor rotated by 120 degrees clockwise relative to the 0 direction.
        :param motor240: motor rotated by 240 degrees clockwise relative to the 0 direction.
        """
        self._motor000 = motor000
        self._motor120 = motor120
        self._motor240 = motor240

        # Initial properties setup
        self._speed = 0.
        self._direction = 0.

    def _update_motors(self):
        self._motor000.speed = self.speed * math.sin(self.direction - math.pi / 3 * 0)
        self._motor120.speed = self.speed * math.sin(self.direction - math.pi / 3 * 2)
        self._motor240.speed = self.speed * math.sin(self.direction - math.pi / 3 * 4)

    @property
    def speed(self) -> float:
        """ Gets or sets the speed of the robot. """
        return self._speed

    @speed.setter
    def speed(self, speed: float):
        self._speed = speed
        self._update_motors()

    @property
    def direction(self) -> float:
        """
        Gets or sets the direction (angle in radians) in which the robot moves.
        The angle value should be within the range [0; 2pi]
        """
        return self._direction

    @direction.setter
    def direction(self, direction: float):
        self._direction = direction
        self._update_motors()

    def stop(self):
        self.speed = 0

    def cleanup(self):
        self._motor000.cleanup()
        self._motor120.cleanup()
        self._motor240.cleanup()


class RetardedMovementController(MovementController):
    """
    Movement controller adjusted to use with the crappy servos set we bought.
    """

    def __init__(self):

        motor000 = MotorDriver(8)  # 1
        motor120 = MotorDriver(10) # 2
        motor240 = MotorDriver(12) # 3

        super().__init__(motor000, motor120, motor240)
