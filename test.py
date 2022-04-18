import os
from time import time
import time

for i in range(0,10):
    os.system(f"gst-launch-1.0 v4l2src device=/dev/video0 num-buffers=1 ! video/x-raw, width=1920, height=1080, framerate=30/1 ! videoconvert ! jpegenc ! filesink location=capture1{i}.jpeg")
    time.sleep(5)
    os.system(f"gst-launch-1.0 v4l2src device=/dev/video2 num-buffers=1 ! video/x-raw, width=1920, height=1080, framerate=30/1 ! videoconvert ! jpegenc ! filesink location=capture2{i}.jpeg")
    time.sleep(5)
    os.system(f"gst-launch-1.0 v4l2src device=/dev/video4 num-buffers=1 ! video/x-raw, width=1920, height=1080, framerate=30/1 ! videoconvert ! jpegenc ! filesink location=capture3{i}.jpeg")
    time.sleep(5)