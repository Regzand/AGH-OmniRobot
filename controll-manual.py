import math
from robot import RetardedMovementController
from robot.drivers import Lsm303dDriver

mc = RetardedMovementController()
lsm = Lsm303dDriver(0x1d)

print("Usage:\n",
      "\tS [-1, 1]\t speed\n",
      "\tD [0, 360)\t direction\n",
      "\tR [-1, 1]\t rotation\n",
      "\tM \t measurements\n",
      "\tstop\n",
      "\texit\n"
)

while True:

    cmd = input("> ").lower().split(" ")

    if cmd[0] == "s":
        mc.speed = float(cmd[1])

    if cmd[0] == "d":
        mc.direction = float(cmd[1]) * 2 * math.pi / 360

    if cmd[0] == "r":
        mc.rotation = float(cmd[1])

    if cmd[0] == "m":
        print("acc: {:+06.2f} : {:+06.2f} : {:+06.2f}".format(
            *lsm.acceleration
        ))
        print("mag: {:+06.2f} : {:+06.2f} : {:+06.2f} (angle xy: {:+03.0f})".format(
            *lsm.magnetic_field,
            lsm.magnetic_field_angle_xy
        ))
        print("tmp: {:.2f}".format(lsm.temperature))

    if cmd[0] == "stop":
        mc.stop()

    if cmd[0] == "exit":
        break

mc.cleanup()
