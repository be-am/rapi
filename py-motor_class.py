#!/user/bin/env python
# coding=utf8
from ast import Expression
from distutils import dir_util
from tkinter import FALSE
from unittest import case
from flask import Flask, render_template, request
from gpiozero import Motor
import RPi.GPIO as GPIO
from time import sleep
import cv2 # Import the OpenCV library
import numpy as np # Import Numpy library
import sys
app = Flask(__name__)
import json
from multiprocessing import shared_memory
import datetime

## pin setting ##
# GPIO.cleanup()

## define function
class MotorControl:
    def __init__(self, max_marker_value):
        self.pwm1 = 14
        self.dir1 = 15
        self.brk1 = 18
        self.speed = 0
        self.freq = 100
        self.max_marker_value = max_marker_value


        self.run_motor = False

    def moveMotor(self, dir, pwm1, dir1, speed): ## dir: 0(forward), 1(backward), 2(left), 3(right)
        
        if dir==0:
            d1 = True
        elif dir==1:
            d1 = False

        GPIO.output(dir1, d1)
    
        pwm1.ChangeDutyCycle(speed)
        
    def stopMotor(self, sec, pwm1): ## stop the motors for input time
        pwm1.ChangeDutyCycle(100)
        sleep(sec)


    def main(self, direction, max_marker_value, target=False):
        with open("/home/pi/webapp/current_location.txt", "r") as file:
            location = file.readlines()[0]

        self.pwm1 = 14
        self.dir1 = 15
        self.brk1 = 18
        self.speed = 0
        self.freq = 100
        print('main function starting...')
        self.run_motor = True
        this_aruco_dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
        this_aruco_parameters = cv2.aruco.DetectorParameters_create()

        marker_value_list = [i for i in range(1, max_marker_value+1)]
     
        i=0
        if direction == 0:
            marker_value_list = marker_value_list[::-1]
          

        try:        
            self.cap1 = cv2.VideoCapture(0)
            self.cap2 = cv2.VideoCapture(2)
            print('all camera captured')
        except:
            self.stop_all()
            print('camera connection failed!')
            sys.exit()
            
        print('video reading complete')

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwm1, GPIO.OUT)
        GPIO.setup(self.dir1, GPIO.OUT)
        GPIO.setup(self.brk1, GPIO.OUT)
        self.pwm1 = GPIO.PWM(self.pwm1, self.freq)
        self.pwm1.start(0)

        while(True):
            
            print(self.run_motor,'self.run_motor')
           
            ret1, frame1 = self.cap1.read()
            ret2, frame2 = self.cap2.read()
            print('ret1 = ', ret1)
            print('ret2 = ', ret2)

            if (np.sum(frame1) == None) or (np.sum(frame2) == None):
                self.stop_all()
                break

            self.moveMotor(direction, self.pwm1, self.dir1, self.speed)
            (corners, ids, rejected) = cv2.aruco.detectMarkers(frame2, this_aruco_dictionary, parameters=this_aruco_parameters)

            
            if target == False:
                if len(corners) > 0 :
                    if ids[0] == marker_value_list[i]:
                        print(ids[0],'ids')
                        print(marker_value_list[i],'marker_value_list')
                        print(i,'i')
                        self.stopMotor(3,self.pwm1)

                        ids = ids.flatten()

                        cv2.imwrite('image{}.jpg'.format(ids[0]),frame1)
                        print('capture!')
                        i+=1
                        if ids[0] == marker_value_list[-1]:
                            self.save_current_location(ids[0])
                            self.stop_all()
                            break    

            else:
                if len(corners) > 0 :
                    if ids[0] == target or ids[0] == max_marker_value or ids[0] ==1 :
                        self.stopMotor(3,self.pwm1)
                    
                        ids = ids.flatten()
                        cv2.imwrite('image{}.jpg'.format(ids[0]),frame1)
                        print('capture!')
                        self.save_current_location(ids[0])
                        self.stop_all()
                        break    
                         
                    
            if cv2.waitKey(1) & 0xFF == ord('q') or (self.run_motor == False):
                self.stop_all()            
                break
    
    def save_current_location(self, location):
        with open("/home/pi/webapp/current_location.txt", "w") as file:
            if location == 0:
                file.write('1')
            elif location == self.max_marker_value:
                file.write('0')
            # loc = str(location)
            # file.write(loc)

        print('save_complete')
            
    def stop_all(self):
        GPIO.cleanup() 
        self.cap1.release()
        self.cap2.release()
        cv2.destroyAllWindows()
        self.pwm1.stop()
        print('clean up all')

    
    @app.route('/')
    def home():
        return render_template('py-motor.htm')

    # @app.route('/motor/forward')
    # def forward():
    #     try:
    #         motor.forward(speed=0.3)
    #     except :
    #         return "fail"

    @app.route('/motor/backward')
    def backward():
        try:
            print('start')
            motorcontroler.main(direction = 0, max_marker_value=motorcontroler.max_marker_value, target=False)
        except :
            return "fail"
        finally:
            return ""

    @app.route('/motor/motor_run')
    def motor_run():
        try:
            
            print('start')
            motorcontroler.main(direction = 1, max_marker_value=motorcontroler.max_marker_value, target=False)
        except :
            return "fail"
        finally:
            return ""

    @app.route('/motor/motor_stop')
    def motor_stop():
        
        motorcontroler.run_motor = False
        return ''

    @app.route('/', methods=['POST'])
    def target_move():
      
        with open("/home/pi/webapp/current_location.txt", "r") as file:
            location = file.readlines()[0]
            print(location,'location')
        marker= request.form.get("marker")
       
        if int(marker) > motorcontroler.max_marker_value:
            (print('error! target number is bigger than max_marker_value'))
        elif int(marker) <= motorcontroler.max_marker_value:   
           
            if int(location) == int(marker):
                print('alread arried')
            elif int(location) < int(marker):
                motorcontroler.main(direction = 1, max_marker_value=motorcontroler.max_marker_value, target=int(marker))
            elif int(location) > int(marker):
                motorcontroler.main(direction = 0, max_marker_value=motorcontroler.max_marker_value, target=int(marker))
        
        
        return render_template('py-motor.htm')    

 
if __name__ == '__main__':

    global motorcontroler
    max_marker_value = 4
    motorcontroler = MotorControl(max_marker_value)

    

    app.run(host='0.0.0.0', port=7000, debug=True)
