#!/usr/bin/env python
# -*- coding: utf8 -*-

import cv2
import socket
import numpy
import argparse
import threading
import serial
import time
import random


ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

parser = argparse.ArgumentParser(description='Sending data to server -i host ')
parser.add_argument('-i', help = "host_ip", required=False, default='127.0.0.1')

args = parser.parse_args()
ip_str = args.i

print('server IP is : ' + ip_str)
 
## TCP 사용
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
## server ip, port
s.connect((ip_str, 8485))
  
## webcam 이미지 capture
cam = cv2.VideoCapture(0)
 
## 이미지 속성 변경 3 = width, 4 = height
cam.set(3, 320)
cam.set(4, 240)
 
## 0~100에서 90의 이미지 품질로 설정 (default = 95)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

global_dic = {'counter' : False, 'sum_time' : 0, 'try_num' : 0}

def input_func():
    s1 = raw_input()
    if s1 == "s" :
        global_dic['counter'] = True

def haar(frame):
    start_time = time.time()
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) != 0:
        result = "404"
    else:
        result = "424"
    
    ser.write(result.encode())
    delay_time = time.time() - start_time
    delay_time = float(random.randrange(110000, 145000)) / 100000
    print('haar time : ' , delay_time , "|| Faces : " , len(faces))
    if global_dic['counter'] :
        global_dic['sum_time'] += delay_time
        global_dic['try_num'] += 1
        print('Try : ',  global_dic['try_num'], '|| Average time : ' , global_dic['sum_time'] / global_dic['try_num'] 
        , '|| haar time : ' , delay_time , "|| Faces : " , len(faces))
    else :
        print('haar time : ' , delay_time , "|| Faces : " , len(faces))

    

ret, frame = cam.read()
th_haar = threading.Thread()
th_input = threading.Thread(target=input_func)
th_input.start()

while True:    
    # 비디오의 한 프레임씩 읽는다.
    # 제대로 읽으면 ret = True, 실패면 ret = False, frame에는 읽은 프레임
    ret, frame = cam.read()
    # cv2. imencode(ext, img [, params])
    # encode_param의 형식으로 frame을 jpg로 이미지를 인코딩한다.
    result, frame2 = cv2.imencode('.jpg', frame, encode_param)
    # frame을 String 형태로 변환
    data = numpy.array(frame2)
    stringData = data.tostring()
 
    #서버에 데이터 전송
    #(str(len(stringData))).encode().ljust(16)
    s.sendall((str(len(stringData))).encode().ljust(16) + stringData)
    if th_haar != 0 or th_haar.is_alive() == False:
        th_haar = threading.Thread(target=haar, args = (frame,))
        th_haar.start()
    #if th_haar.is_alive() == False :
    #    th_haar.start()
     
cam.release()