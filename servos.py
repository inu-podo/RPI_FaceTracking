import RPi.GPIO as GIPO
import time
pin1 = 18
pin2 = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)

p1 = GPIO.PWM(pin1, 50)
p2 = GPIO.WPM(pin2, 50)

p1.start(2.5)
p2.start(2.5)

try:
    while True:
        #7.5 90%     2.5 0%    12.5 180%
        p1.ChangeDutyCycle(7.5)
        print("somethings happening 1")
        time.sleep(1)
        p1.ChangeDutyCycle(12.5)
        print("somethings happening 1")
        time.sleep(1)
        p1.ChangeDutyCycle(2.5)
        print("somethings happening 1")
        time.sleep(3)
except KeyboardInterrupt:
    p1.stop()
    p2.stop()
    
GPIO.cleanup()