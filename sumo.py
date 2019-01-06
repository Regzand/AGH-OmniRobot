import signal
import sys
import math
from time import sleep
from robot import RetardedMovementController
from robot.drivers import LSM303DDriver
from robot.drivers import VL53L1XDriver

mc = RetardedMovementController()

# SIGINT setup
def signal_handler(sig, frame):
    mc.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

lsm = LSM303DDriver(0x1d)
vl = VL53L1XDriver(0x29)
vl.start()


attack_scaling = 1
threshold = 30

searching = True
action = False

while True:

    dist = vl.distance
    if dist < threshold:
        searching = False
        action = True

    else:
        searching = True
        action = False

    if searching:
        mc.speed = 0
        mc.rotation = 0.8

    else:
        mc.speed = 0.8 * attack_scaling
        mc.rotation = 0

    sleep(0.2)


mc.cleanup()