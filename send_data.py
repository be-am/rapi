import requests
import os
import time

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