from MovementController import RetardedMovementController
import time
import math

mc = RetardedMovementController()

mc.speed = 0.5
mc.direction = 0

while True:
	time.sleep(1)
	mc.direction += math.pi / 3

mc.stop()
mc.cleanup()
