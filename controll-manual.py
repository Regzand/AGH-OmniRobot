from MovementController import RetardedMovementController

mc = RetardedMovementController()

print("Usage:\n", "\tS [-1, 1]\t speed\n", "\tD [0, 360)\t direction\n", "\tR [-1, 1]\t rotation\n", "\tstop\n", "\texit\n")

while True:

    cmd = input("> ").split(" ")

    if cmd[0] == "S":
        mc.speed = float(cmd[1])

    if cmd[0] == "D":
        mc.direction = float(cmd[1])

    if cmd[0] == "R":
        mc.rotation = float(cmd[1])

    if cmd[0] == "stop":
        mc.stop()

    if cmd[0] == "exit":
        break

mc.cleanup()
