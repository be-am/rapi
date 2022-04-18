import RPi.GPIO as GPIO
import time 
from re import sub
import cv2
import time 
from datetime import datetime

class MotorControl:
    def __init__(self):
        self.pwm1 = 26
        self.dir1 = 22
        # self.brk1 = 26
        self.speed = 0
        self.freq = 255
        self.forward = True
        
    def main(self):
        date = datetime.today()
        date = date.strftime('%Y,%m,%d,%H,%M')
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwm1, GPIO.OUT)
        GPIO.setup(self.dir1, GPIO.OUT)
        # GPIO.setup(self.brk1, GPIO.OUT)

        self.pwm1 = GPIO.PWM(self.pwm1, self.freq)
        self.pwm1.stop()
        self.pwm1.start(0)

        self.moveMotor(self.forward, self.pwm1, self.dir1, self.speed)

        cap1 = cv2.VideoCapture(0)
        ret1, frame1=cap1.read()
        cv2.imwrite(f'/home/pi/webapp/img/f1/{date}__frame1.png', frame1)
        cap1.release()
        del cap1
     
        self.stopMotor(5,self.pwm1)
      
      
        self.moveMotor(self.forward, self.pwm1, self.dir1, self.speed)
        self.cap2 = cv2.VideoCapture(2)
        self.cap2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.cap2.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
        self.cap2.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
        ret1, frame2=self.cap2.read()
        cv2.imwrite(f'/home/pi/webapp/img/f2/{date}__frame2.png', frame2)
        
        self.cap2.release()
        del self.cap2

        self.stopMotor(5,self.pwm1)

        self.moveMotor(self.forward, self.pwm1, self.dir1, self.speed)

        self.cap3 = cv2.VideoCapture(4)
        self.cap3.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.cap3.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
        self.cap3.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
        ret1, frame3=self.cap3.read()
        cv2.imwrite(f'/home/pi/webapp/img/f3/{date}__frame3.png', frame3)
        self.cap3.release()
        del self.cap3

        self.stopMotor(5,self.pwm1)
        self.moveMotor(self.forward, self.pwm1, self.dir1, self.speed)
        time.sleep(30) 
        self.stopMotor(5,self.pwm1)
        self.pwm1.stop()

        GPIO.cleanup() 
        print('stop')

    def moveMotor(self, dir, pwm1, dir1, speed): 
            if dir==0:
                d1 = True
            elif dir==1:
                d1 = False  
            print('start')    

            GPIO.output(dir1, d1)
            pwm1.ChangeDutyCycle(speed) 
            time.sleep(10) 

    def stopMotor(self, sec, pwm1):
        print('pause')
        pwm1.ChangeDutyCycle(100)
        time.sleep(sec)        

if __name__ == '__main__':
    # time.sleep(10)

    motorcontroler = MotorControl()
    motorcontroler.main()