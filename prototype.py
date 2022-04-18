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
from multiprocessing import shared_memory
import datetime
import requests
import os
from glob import glob
import shutil
import yaml

class MotorControl:
    def __init__(self, max_marker_value):
        self.pwm1 = 21
        self.dir1 = 22
        self.brk1 = 26
        self.speed = 0
        self.freq = 100
        self.image_path = '/home/pi/webapp/image'
        self.max_marker_value = max_marker_value
        self.run_motor = False
        self.read_yaml()

        # self.direction = self.data['direction']
        # self.house = self.data['house']
        # self.line = self.data['line']
        # self.location = self.data['location']
 
    def read_yaml(self):
        with open('/home/pi/webapp/data.yaml') as fr : 
            self.data = yaml.load(fr, Loader=yaml.FullLoader)

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
        
    def saveimg(self, location):
        try:
            self.cap2 = cv2.VideoCapture(2)
            print('cap2 compl')
        except:
            print('camera2 error!! need reboot')    
        print(self.cap2)
        self.cap2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.cap2.set(cv2.CAP_PROP_FRAME_WIDTH,1920) 
        self.cap2.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
        ret2, frame2 = self.cap2.read()
        if (np.sum(frame2) == None):
            print('camera2 frame error!')
       
        cv2.imwrite(f'/home/pi/webapp/image/cam_1_{location}.jpg',frame2)
        self.cap2.release()
        del self.cap2
        
        try:
            self.cap3 = cv2.VideoCapture(4)
            print('cap4 compl')
        except:
            ('camera4 error!! need reboot')   
        print('1')        
        self.cap3.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.cap3.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
        self.cap3.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
        ret3, frame3 = self.cap3.read()
        print('2') 
        cv2.imwrite(f'/home/pi/webapp/image/cam_2_{location}.jpg',frame3)
        self.cap3.release()
        del self.cap3
        print('3') 
    def run_forward(self, max_marker_value):
        self.pwm1 = 21
        self.dir1 = 22
        self.brk1 = 26
        self.speed = 0
        self.freq = 100
        print('forward main function starting...')
        
        if self.data["location"] == 0:
            pre_location = self.data["location"]

        else:
            pre_location = self.data["location"] +1

        self.run_motor = True
        this_aruco_dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
        this_aruco_parameters = cv2.aruco.DetectorParameters_create()
       
        marker_value_list = [i for i in range(pre_location, max_marker_value+1)]
        
        i=0
        tens = pre_location//10     
       
        if tens == 0 and pre_location%10 !=0:
            tens +=1
                  
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwm1, GPIO.OUT)
        GPIO.setup(self.dir1, GPIO.OUT)
        GPIO.setup(self.brk1, GPIO.OUT)
        self.pwm1 = GPIO.PWM(self.pwm1, self.freq)
        self.pwm1.start(0)

        ones_list = [i for i in range(pre_location,10)]
        print(f'ones_list = {ones_list}')   
        self.cap1 = None
        if not os.path.exists(self.image_path):
            os.makedirs(self.image_path)
            print('folder compl')

        print(f'marker_value_list = {marker_value_list}')            
        while(True):
            if self.cap1 == None:
                try:
                    self.cap1 = cv2.VideoCapture(0)
                    print('cap1 compl')
                # self.cap1.set(cv2.CAP_PROP_FRAME_WIDTH,2560)
                # self.cap1.set(cv2.CAP_PROP_FRAME_HEIGHT,1440)
                except:
                    self.stop_all()
                    print('camera connection failed!')
                    os.system('sudo reboot -n')
            ret1, frame1 = self.cap1.read()
            self.moveMotor(1, self.pwm1, self.dir1, self.speed)
            
            if (np.sum(frame1) == None) :
                print('frame reading failed')
                self.stop_all()
                os.system('sudo reboot -n')
                

            (corners, ids, rejected) = cv2.aruco.detectMarkers(frame1, this_aruco_dictionary, parameters=this_aruco_parameters)

            if np.sum(ids) != None:
                
                if ids[0, 0] == ones_list[0]:
                    print(ids[0, 0], 'marker num!')
                    if ids[0,0] == 0:
                        
                        ones_list.remove(0)
                        tens +=1
                        location = (tens-1) * 10
                        self.stopMotor(1,self.pwm1)
                        self.cap1.release()
                        del self.cap1
                        self.cap1 = None
                         
                        self.saveimg(location)
                        print(tens)
                        input(type(tens))
                        if type(tens) is not int:
                            location = location.item()
                       
                        self.save_location(location)
                        marker_value_list.remove(location)
                        print(f'marker_value_list = {marker_value_list}') 
                        print(f'captured location = forward {location}!')
                        if location == self.max_marker_value:
                            self.change_direction(location)
                            self.stop_all()
                            break
                    else:# ids[0,0] != 0 and ids[0,0] in ones_list:
                     
                        location = (tens-1) * 10 + ids[0,0]
                        ones_list.remove(ids[0,0])
                        print(ones_list,'removed ones list')
                        print(location)
                        print(marker_value_list)
                        if location in marker_value_list:
                            marker_value_list.remove(location)
                            print(f'marker_value_list = {marker_value_list}') 
                            self.stopMotor(1,self.pwm1)
                            ids = ids.flatten()
                            self.cap1.release()
                            del self.cap1
                            self.cap1 = None
                            
                            if type(tens) is not int:
                                location = location.item()
                            self.saveimg(location)
                            self.save_location(location)
                            print(f'captured location = forward {location}!')
                            i+=1
                            if location == self.max_marker_value:
                                self.change_direction(location)
                                self.stop_all()
                                break

            if len(ones_list) == 0:
                ones_list = [i for i in range(0,10)]
                
    def run_backward(self, max_marker_value):
        self.pwm1 = 21
        self.dir1 = 22
        self.brk1 = 26
        self.speed = 0
        self.freq = 100
        print('back main function starting...')

        if self.data["location"] == max_marker_value:
            pre_location = self.data["location"]

        else:
            pre_location = self.data["location"] -1


        self.run_motor = True
        this_aruco_dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
        this_aruco_parameters = cv2.aruco.DetectorParameters_create()
        marker_value_list = [i for i in range(0, pre_location+1)]
        marker_value_list = marker_value_list[::-1]
        print(f'marker_value_list = {marker_value_list}') 
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwm1, GPIO.OUT)
        GPIO.setup(self.dir1, GPIO.OUT)
        GPIO.setup(self.brk1, GPIO.OUT)
        self.pwm1 = GPIO.PWM(self.pwm1, self.freq)
        self.pwm1.start(0)

        tens = pre_location // 10
        ones_offset = pre_location % 10
        ones_list = [i for i in range(0,10)]
        ones_list = ones_list[:ones_offset+1]
        print(f'ones_list = {ones_list}') 

        i=0
        self.cap1 = None
        if not os.path.exists(self.image_path):
            os.makedirs(self.image_path)
            print('folder compl') 
        while(True):
            if self.cap1 == None:
                try:
                    self.cap1 = cv2.VideoCapture(0)
                    print('cap1 compl')
                except:
                    self.stop_all()
                    print('camera connection failed!')
                    sys.exit()
            ret1, frame1 = self.cap1.read()
            self.moveMotor(1, self.pwm1, self.dir1, self.speed)
            if (np.sum(frame1) == None):
                print('frame reading failed')
                self.stop_all()
                break

            (corners, ids, rejected) = cv2.aruco.detectMarkers(frame1, this_aruco_dictionary, parameters=this_aruco_parameters)
            # print(type(ids[0, 0]), '16236')
            if np.sum(ids) != None:
                location = tens * 10 + ids[0,0]
                if location == marker_value_list[0]:
                    if ids[0, 0] in ones_list:
                        if ids[0,0] == 0:
                            ones_list.remove(0)
                            self.stopMotor(1,self.pwm1)
                            self.cap1.release()
                            del self.cap1
                            self.cap1 = None
                            #create image folder
                            
                            
                            if type(tens) is not int:
                                location = location.item()
                            self.saveimg(location)
                            
                            self.save_location(location)
                            marker_value_list.remove(location)
                            print(f'marker_value_list = {marker_value_list}') 
                            print(f'captured location = back {location}!')
                            tens -=1
                            i +=1
                            if location == 0:
                                self.change_direction(location)
                                self.stop_all()
                                break

                        else:# ids[0,0] != 0 and ids[0,0] in ones_list:
                            ones_list.remove(ids[0,0])
                            marker_value_list.remove(location)
                            print(f'marker_value_list = {marker_value_list}') 
                            self.stopMotor(1,self.pwm1)
                            ids = ids.flatten()
                            self.cap1.release()
                            del self.cap1
                            self.cap1 = None
                            if type(tens) is not int:
                                location = location.item()
                            self.saveimg(location)
                            self.save_location(location)
                            print(f'captured location = back {location}!')
                            i+=1

            if len(ones_list) == 0:
                ones_list = [i for i in range(0,10)]


    def save_location(self, location):

        print(self.data["location"])
        print(type(location))
        self.data["location"] = location
        
        print(self.data["location"], 'convert loc')
        print(self.data, 'convert data')
   

        with open('/home/pi/webapp/data.yaml', 'w') as fw:
            yaml.dump(self.data, fw)       
        

    def change_direction(self, location):
        
        with open('/home/pi/webapp/data.yaml', 'w') as fw:
            if location == 0:
                self.data["direction"] = 1
            elif location == self.max_marker_value:
                self.data["direction"] = 0
            
            yaml.dump(self.data, fw)  
                
    def stop_all(self):
        GPIO.cleanup()

        self.pwm1.stop()
        print('clean up all')
       
        
    #예외 처리 할 것들 생각 해보기
    # 1. 이미지 파일 없을 떄 예외처리  
    # 2. send_data를 보내는 경우에 대해 잘 생각 해봐야함(중간에 라파이가 꺼질경우 이미지의 개수를 세서 send_data를 보낼지 말지에 대한 고려도 해봐야함)
    def send_data(self):
        
        url = "http://192.168.0.46:5050/upload"
        
        date = datetime.datetime.today()
        date = date.strftime('%Y,%m,%d,%H,%M')
        
        #라즈베리파일 별로 house_id와 line_id가 정해져 있기 떄문에 각 id들을 txt파일에 저장해놓고 send_data를 호출 할 때 두 id 값을 불러와서 서버단에서 두가지를 저장할 수 있게 함
        # with open('/home/pi/webapp/house.txt', 'r') as house: 
        #     house_id = house.readline()
        # with open('/home/pi/webapp/line.txt', 'r') as line: 
        #     line_id = line.readline()
        house_id = self.data["house"]
        line_id = self.data["line"]
        #폴더 안의 모든 이미지의 이름을 리스트로 저장
        image_names = os.listdir(self.image_path)   
        
        for image in image_names:
            #extract marker_id (마커가 이미지 파일의 이름으로 저장되어 있기 때문에 확장자 파일을 삭제하여 파일의 이름으로부터 마커를 받아옴)
            image_num = image.split('_')[1]
            index = image.index('.')
            location = image[:index]
                
            # payload 단에 dictionary 방식으로 데이터 값들을 쌓아줌
            payload = {'date':f'{date}','house_id':f'{house_id}', 'line_id':f'{line_id}','image_num':f'{image_num}','marker_id':f'{location}'}
            print(payload)
            files=[
            ('file',(f'{date}_{house_id}_{line_id}_{image_num}_{location} img.PNG',open(f'/home/pi/webapp/image/{image}','rb'),'application/octet-stream'))
            ]
            headers = {}        
            
            # 서버단에 데이터 전송
            response = requests.request("POST", url, headers=headers, data=payload, files=files)
        
        # shutil.rmtree에 원래는 경로 image_path 넣으면 됨 
        # 다 돌리고 image 파일 사라지는걸 가정함
        shutil.rmtree(self.image_path)
        
    
    def main(self):

        # if self.location == 0 or self.location == motorcontroler.max_marker_value:
        if self.data["direction"] == 1:
            try:
                motorcontroler.run_forward(max_marker_value=motorcontroler.max_marker_value)
                motorcontroler.send_data()
            except :
                return "fail"
        elif self.data["direction"] == 0:
            try:
                motorcontroler.run_backward(max_marker_value=motorcontroler.max_marker_value)
                motorcontroler.send_data()
            except :
                return "fail"


if __name__ == '__main__':
    global motorcontroler
    max_marker_value = 13
    motorcontroler = MotorControl(max_marker_value)
    motorcontroler.main()