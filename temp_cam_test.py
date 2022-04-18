from re import sub
import cv2
import time 
from datetime import datetime
import os
import subprocess

import sys



# this_aruco_dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
# this_aruco_parameters = cv2.aruco.DetectorParameters_create()
# os.system('v4l2-ctl --device /dev/video0 --set-fmt-video=width=1920,height=1280,pixelformat=MJPG --stream-mmap --stream-to=/home/pi/frame4.jpg --stream-count=1')
# subprocess.call("v4l2-ctl --device /dev/video0 --set-fmt-video=width=1280,height=720,pixelformat=MJPG --stream-mmap --stream-to=/home/pi/frame4.jpg --stream-count=1",shell=True)
while True:
 
    # print(datetime.now())
    # time.sleep(0.3)
    cap1 = cv2.VideoCapture(0)
    ret1, frame1=cap1.read()
    cv2.imwrite('/home/pi/webapp/frame1.png', frame1)
    cap1.release()
    del cap1

    # cap1 = cv2.VideoCapture(0)
    # cap1.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    # cap1.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
    # cap1.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
    print('cap1 compl')
    print(ret1)
    if ret1:
        try:
            cap2 = cv2.VideoCapture(2)
            print('cap2 compl')

        # self.cap1.set(cv2.CAP_PROP_FRAME_WIDTH,2560)
        # self.cap1.set(cv2.CAP_PROP_FRAME_HEIGHT,1440)
        except:
          
            print('camera connection failed!')
            sys.exit()

        cap2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        cap2.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
        cap2.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
        ret2, frame2=cap2.read()    
        cv2.imwrite('/home/pi/webapp/frame2.png', frame2)    
        # t1 = time.time()
        # os.system("gst-launch-1.0 v4l2src device=/dev/video2 num-buffers=1 ! video/x-raw, width=1920, height=1080, framerate=30/1 ! videoconvert ! jpegenc ! filesink location=/home/pi/capture2.jpeg")
        # cap2=subprocess.Popen(["v4l2-ctl --device=/dev/video2 --set-fmt-video=width=1920,height=1080,pixelformat=MJPG --stream-mmap --stream-to=/home/pi/frame2.png --stream-count=1"], shell=True)
        # cap2=subprocess.Popen(["gst-launch-1.0 v4l2src device=/dev/video2 num-buffers=1 ! video/x-raw, width=1920, height=1080, framerate=30/1 ! videoconvert ! jpegenc ! filesink location=/home/pi/capture2.jpeg"], shell=True)
        # # print(cap2)
        # cap2.wait(timeout=3000)
        # print(cap2.pid)
        # time.sleep(20)
        # cap2.terminate()
        # cap2.kill()
        # t2 = time.time()
        # print(f'cap 2, {t2-t1}')
        # os.system("gst-launch-1.0 v4l2src device=/dev/video4 num-buffers=1 ! video/x-raw, width=1920, height=1080, framerate=30/1 ! videoconvert ! jpegenc ! filesink location=/home/pi/capture3.jpeg")
        # cap3=subprocess.Popen(["v4l2-ctl --device=/dev/video4 --set-fmt-video=width=1920,height=1080,pixelformat=MJPG --stream-mmap --stream-to=/home/pi/frame3.png --stream-count=1"], shell=True)
        # cap3=subprocess.Popen(["gst-launch-1.0 v4l2src device=/dev/video4 num-buffers=1 ! video/x-raw, width=1920, height=1080, framerate=30/1 ! videoconvert ! jpegenc ! filesink location=/home/pi/capture3.jpeg"], shell=True)
        
        # print(cap3)
        
        # cap3.wait(timeout=3000)
        # print(cap3.pid)
        # time.sleep(20)
        # cap3.terminate()
        # cap3.kill()
        # subprocess.call("v4l2-ctl --device /dev/video4 --set-fmt-video=width=1920,height=1080,pixelformat=MJPG --stream-mmap --stream-to=/home/pi/frame3.jpg --stream-count=1",shell=True)
        # print('cap 3')
        # subprocess.Popen.kill()
        # cv2.imwrite('/home/pi/webapp/frame2.png', frame2)
        # cv2.imwrite('/home/pi/webapp/frame3.png', frame2)
        # cv2.imwrite('/home/pi/webapp/frame4.png', frame2)
        cap2.release()
        del cap2

        # cap3 = cv2.VideoCapture(4)
        # cap3.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        # cap3.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
        # cap3.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
        # ret3, frame3=cap3.read()
        # cv2.imwrite('frame3.png', frame3)
        # cap3.release()
        # del cap3
        

        # cv2.imshow('frame1', frame1)
        # cv2.imshow('frame2', frame2)
        # cv2.imshow('frame3', frame3)
        
        # cv2.imwrite('frame1.png', frame1)
        
        # break

        # (corners, ids, rejected) = cv2.aruco.detectMarkers(frame1, this_aruco_dictionary, parameters=this_aruco_parameters)
        # time.sleep(1)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    else:
        break