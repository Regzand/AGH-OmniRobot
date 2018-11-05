from robot import RetardedMovementController
import time
import math

mc = RetardedMovementController()

def shape(speed, duration, angle, reps = math.inf, direction = 0):
	mc.speed = speed
	mc.direction = direction
	for i in range(reps):
		time.sleep(duration)
		mc.direction += angle

time.sleep(2)

shape(0.6, 1, math.pi / 2,  4)
shape(0.6, 1, math.pi / -2, 4, math.pi / 2)
shape(0.6, 1, math.pi / 3, 6)

mc.speed = 0
mc.rotation = 1

time.sleep(5)

mc.stop()
mc.cleanup()
