import math
from MovementController import RetardedMovementController

mc = RetardedMovementController()

print("Usage:\n", "\tS [-1, 1]\t speed\n", "\tD [0, 360)\t direction\n", "\tR [-1, 1]\t rotation\n", "\tstop\n", "\texit\n")

while True:

    cmd = input("> ").lower().split(" ")

    if cmd[0] == "s":
        mc.speed = float(cmd[1])

    if cmd[0] == "d":
        mc.direction = float(cmd[1]) * 2 * math.pi / 360

    if cmd[0] == "r":
        mc.rotation = float(cmd[1])

    if cmd[0] == "stop":
        mc.stop()

    if cmd[0] == "exit":
        break

mc.cleanup()
