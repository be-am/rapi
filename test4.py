#!/user/bin/env python
# coding=utf8
from ast import Expression
from distutils import dir_util
from tkinter import FALSE
from unittest import case
from flask import Flask, render_template, request
from gpiozero import Motor
import RPi.GPIO as GPIO
from time import sleep, time
import cv2 # Import the OpenCV library
import numpy as np # Import Numpy library
import sys
app = Flask(__name__)
import json
from multiprocessing import shared_memory
import datetime

class MotorControl:
    def __init__(self, max_marker_value):
        self.pwm1 = 14
        self.dir1 = 15
        self.brk1 = 18
        self.speed = 0
        self.freq = 100
        self.max_marker_value = max_marker_value
        self.run_motor = False

    def moveMotor(self, dir, pwm1, dir1, speed): 
        if dir==0:
            d1 = True
        elif dir==1:
            d1 = False

        GPIO.output(dir1, d1)
        pwm1.ChangeDutyCycle(speed)
        
    def stopMotor(self, sec, pwm1):
        pwm1.ChangeDutyCycle(100)
        sleep(sec)


    def run_forward(self, max_marker_value):

        self.pwm1 = 14
        self.dir1 = 15
        self.brk1 = 18
        self.speed = 0
        self.freq = 100
        print('main function starting...')
        self.run_motor = True
        this_aruco_dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
        this_aruco_parameters = cv2.aruco.DetectorParameters_create()

        marker_value_list = [i for i in range(0, max_marker_value+1)]
     
        i=0
        tens = 0

        try:        
            self.cap1 = cv2.VideoCapture(0)
            self.cap2 = cv2.VideoCapture(2)
            self.cap2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            self.cap2.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
            self.cap2.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
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

        
        ones_list = [i for i in range(0,10)]

        while(True):
           
            ret1, frame1 = self.cap1.read()
            ret2, frame2 = self.cap2.read()

            self.moveMotor(1, self.pwm1, self.dir1, self.speed)

            if (np.sum(frame1) == None) or (np.sum(frame2) == None):
                print('frame reading failed')
                self.stop_all()
                break
       
            (corners, ids, rejected) = cv2.aruco.detectMarkers(frame2, this_aruco_dictionary, parameters=this_aruco_parameters)
            

            if np.sum(ids) != None:
                if ids[0, 0] in ones_list:
                    if ids[0,0] == 0:
                        ones_list.remove(0)
                        tens +=1

                        location = (tens-1) * 10
                        self.stopMotor(1,self.pwm1)
                        cv2.imwrite('image{}.jpg'.format(location),frame1)
                        marker_value_list.remove(location)
                        print(f'captured location = {location}!')
                        if location == self.max_marker_value:
                            self.save_current_location(location)
                            self.stop_all()
                            break    

                    else:# ids[0,0] != 0 and ids[0,0] in ones_list:
                        location = (tens-1) * 10 + ids[0,0]
                        ones_list.remove(ids[0,0])

                        if location in marker_value_list:
                            marker_value_list.remove(location)
                            print(marker_value_list)
                            self.stopMotor(1,self.pwm1)

                            ids = ids.flatten()
                            cv2.imwrite('image{}.jpg'.format(location),frame1)
                            print(f'captured location = {location}!')
                            i+=1

                            if location == self.max_marker_value:
                                self.save_current_location(location)
                                self.stop_all()
                                break    

            if len(ones_list) == 0:
                ones_list = [i for i in range(0,10)]


    def run_backward(self, max_marker_value):

        self.pwm1 = 14
        self.dir1 = 15
        self.brk1 = 18
        self.speed = 0
        self.freq = 100
        print('main function starting...')
        self.run_motor = True
        this_aruco_dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
        this_aruco_parameters = cv2.aruco.DetectorParameters_create()

        marker_value_list = [i for i in range(0, max_marker_value+1)]
        marker_value_list = marker_value_list[::-1]
     


        try:        
            self.cap1 = cv2.VideoCapture(0)
            self.cap2 = cv2.VideoCapture(2)
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

        tens = max_marker_value // 10
        ones_offset = max_marker_value % 10
        
        ones_list = [i for i in range(0,10)]
        ones_list = ones_list[:ones_offset+1]

        print('ones_list = ', ones_list)
        i=0

        while(True):
           
            ret1, frame1 = self.cap1.read()
            ret2, frame2 = self.cap2.read()

            self.moveMotor(1, self.pwm1, self.dir1, self.speed)

            if (np.sum(frame1) == None) or (np.sum(frame2) == None):
                print('frame reading failed')
                self.stop_all()
                break
       
            (corners, ids, rejected) = cv2.aruco.detectMarkers(frame2, this_aruco_dictionary, parameters=this_aruco_parameters)
            

            if np.sum(ids) != None:
                location = tens * 10 + ids[0,0]
                if location == marker_value_list[0]:
                    if ids[0, 0] in ones_list:
                        if ids[0,0] == 0:
                            ones_list.remove(0)
                            self.stopMotor(1,self.pwm1)
                            cv2.imwrite('image{}.jpg'.format(location),frame1)
                            marker_value_list.remove(location)
                            print(f'captured location = {location}!')
                            tens -=1
                            i +=1
                            
                            if location == 0:
                                self.save_current_location(location)
                                self.stop_all()
                                break 

                        else:# ids[0,0] != 0 and ids[0,0] in ones_list:
                            ones_list.remove(ids[0,0])
                            marker_value_list.remove(location)
                            print(marker_value_list)
                            self.stopMotor(1,self.pwm1)

                            ids = ids.flatten()
                            cv2.imwrite('image{}.jpg'.format(location),frame1)
                            print(f'captured location = {location}!')
                            i+=1  

            if len(ones_list) == 0:
                ones_list = [i for i in range(0,10)]

    def save_current_location(self, location):
        with open("/home/pi/webapp/current_location.txt", "w") as file:
            if location == 0:
                file.write('1')
            elif location == self.max_marker_value:
                file.write('0')
            
    def stop_all(self):
        GPIO.cleanup() 
        self.cap1.release()
        self.cap2.release()
        cv2.destroyAllWindows()
        self.pwm1.stop()
        print('clean up all')

    def main(self):
        with open("/home/pi/webapp/current_location.txt", "r") as f:
            loc = int(f.readline())

        if loc == 1:
            try:
                print('start')
                motorcontroler.run_forward(max_marker_value=motorcontroler.max_marker_value)
            except :
                return "fail"

        elif loc == 0:
            try:
                print('start')
                motorcontroler.run_backward(max_marker_value=motorcontroler.max_marker_value)
            except :
                return "fail"

 
if __name__ == '__main__':

    global motorcontroler
    max_marker_value = 4
    motorcontroler = MotorControl(max_marker_value)
    motorcontroler.main()
