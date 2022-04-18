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
import requests

class MotorControl:
    def __init__(self, max_marker_value):
  
        self.max_marker_value = max_marker_value


    def run_forward(self, max_marker_value, forward):

        self.pwm1 = 21
        self.dir1 = 22
        self.brk1 = 26
        self.speed = 0
        self.freq = 100
        print('forward main function starting...')
      
        this_aruco_dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
        this_aruco_parameters = cv2.aruco.DetectorParameters_create()

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwm1, GPIO.OUT)
        GPIO.setup(self.dir1, GPIO.OUT)
        GPIO.setup(self.brk1, GPIO.OUT)
        self.pwm1 = GPIO.PWM(self.pwm1, self.freq)
        
   
        marker_value_list = [i for i in range(0, max_marker_value+1)]

        if forward == False:
           
            marker_value_list = marker_value_list[::-1]
         
    
        
        section = 0
        self.cap1 = None
        print(marker_value_list, 'marker_value_list')

        while(True):
            if self.cap1 == None:
                try:        
                    self.cap1 = cv2.VideoCapture(0)
                    print('cap1(marker) complete')
                except:
                    self.stop_all()
                    print('camera connection failed!')
                    sys.exit()
            ret1, frame1 = self.cap1.read()        
            
            if (np.sum(frame1) == None) :
                print('frame reading failed')
                self.stop_all()
                break
       
            (corners, ids, rejected) = cv2.aruco.detectMarkers(frame1, this_aruco_dictionary, parameters=this_aruco_parameters)
       
            
            self.pwm1.start(0)
            self.moveMotor(forward, self.pwm1, self.dir1, self.speed)
   
            if np.sum(ids) != None:
                print(ids, 'ids')
                if ids[0,0] == marker_value_list[-1]:
                    self.cap1.release()
                    del self.cap1
                    self.save_current_location( marker_value_list[-1])
                    self.stop_all()
                    self.send_data()
                    print
                    break

                if ids[0,0] == marker_value_list[section]:
                    self.cap1.release()
                    del self.cap1
                    self.cap1 = None
                    for j in range(5):
                        sleep(5)
                        self.stopMotor(2,self.pwm1)
                        

                        if forward ==True:
                            self.saveimg(ids[0,0], j+1)
                            print(f'captured location = forward {ids[0,0]}_{j+1}!')
                        elif forward ==False:
                            self.saveimg(ids[0,0]-1, 5 -j)
                            print(f'captured location = backward {ids[0,0]}_{5-j}!')    
                        
                        if j ==4:
                            break
                        self.moveMotor(forward, self.pwm1, self.dir1, self.speed)
                            
                    section +=1

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

    def saveimg(self, section, num):

        self.cap2 = cv2.VideoCapture(2)
        self.cap2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.cap2.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
        self.cap2.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
        ret2, frame2 = self.cap2.read()
        cv2.imwrite(f'camera2__{section}_{num}.jpg',frame2)
        self.cap2.release()
        del self.cap2

        self.cap3 = cv2.VideoCapture(4)
        self.cap3.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.cap3.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
        self.cap3.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
        ret2, frame3 = self.cap3.read()
        cv2.imwrite(f'camera3__{section}_{num}.jpg',frame3)
        self.cap3.release()
        del self.cap3            

    def send_data(self):
        url = "http://192.168.0.46:5050/upload"
        house_id = "1"
        marker_id = "2"
        # url 받고
        #request 코드는 기존 코드에 합치기 때문에 house_id, marker_id 받는 방식은 따로 정해야함
        house_id_list = [i for i in range(0, 4)]
        marker_list = [i for i in range(0, 4)]
        # fileList = os.listdir('/')
        # fileLoad = os.getcwd()
        for house_id, marker_id in zip(house_id_list, marker_list):
            payload={'house_id':f'{house_id}', 'marker_id':f'{marker_id}'}
            print(payload)
            files=[
                ('file',(f'{house_id}_{marker_id}_img.PNG', open(f'/home/pi/frame{house_id}.png','rb'),'application/octet-stream')),
            ]
            headers = {}
            response = requests.request("POST", url, headers=headers, data=payload, files=files)


    def save_current_location(self, location):
        with open("/home/pi/webapp/current_location.txt", "w") as file:
            if location == 0:
                file.write('1')
            elif location == 9:
                file.write('0')
            elif location == 10:
                file.write('10')
   
            
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
                print('start_forward')
                # self.save_current_location(11)
                self.run_forward(max_marker_value=self.max_marker_value, forward=True)
            except :
                return "fail"

        elif loc == 0:
            # try:
            print('start_backward')
            # self.save_current_location(10)
            self.run_forward(max_marker_value=self.max_marker_value, forward=False)
        # except :
            print('fail!')
            return "fail"

        # elif loc == 10:
        #     try:
        #         print('back_to_start')
        #         self.save_current_location(self, 20)
        #         motorcontroler.run_forward(max_marker_value=self.max_marker_value, forward=False)
        #     except :
        #         return "fail"        

 
if __name__ == '__main__':

    global motorcontroler
    max_marker_value = 4
    motorcontroler = MotorControl(max_marker_value)
    motorcontroler.main()
