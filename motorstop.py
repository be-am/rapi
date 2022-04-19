from gpiozero import Motor
import RPi.GPIO as GPIO
import time
pwm1 = 27
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm1, GPIO.OUT)
# GPIO.output(21, GPIO.LOW)
# # time.sleep(5)
# GPIO.output(21, GPIO.HIGH)
# time.sleep(5)
# GPIO.output(21, GPIO.LOW)
# time.sleep(5)
# GPIO.output(21, GPIO.HIGH)
# time.sleep(5)
# pwm1 = GPIO.PWM(pwm1,100)
pwm1 = GPIO.PWM(pwm1, 100)
# # pwm1.start(0)
# # time.sleep(3)
pwm1.stop()
# GPIO.output(pwm1, GPIO.HIGH)

GPIO.cleanup()
# pwm1.stop()



print('clean up all')