import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
p = GPIO.PWM(13, 100)
p.start(0)

try:
    while 1:
        p.ChangeDutyCycle(0)
except KeyboardInterrupt:
    pass
#p.stop()
#GPIO.cleanup()
