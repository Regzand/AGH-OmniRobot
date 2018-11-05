import RPi.GPIO as GPIO
import signal
import sys

# const
FREQUENCY = 50
MIN_DUTY_CYCLE = 5
MAX_DUTY_CYCLE = 10
OFF_DUTY_CYCLE = (MIN_DUTY_CYCLE + MAX_DUTY_CYCLE) / 2

# GPIO setup
GPIO.setmode(GPIO.BOARD)

# channel setup
channel = int(input("Enter channel number: "))
GPIO.setup(channel, GPIO.OUT)
p = GPIO.PWM(channel, FREQUENCY)
p.start(OFF_DUTY_CYCLE)

# SIGINT setup
def signal_handler(sig, frame):
	p.stop()
	GPIO.cleanup()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# main loop
while True:
	duty_cycle = float(input("Enter duty cycle (-/+ 100): "))

	p.ChangeDutyCycle((duty_cycle + 100) / 200 * (MAX_DUTY_CYCLE - MIN_DUTY_CYCLE) + MIN_DUTY_CYCLE)
