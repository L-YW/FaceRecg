#!/usr/bin/env python
# -*- coding: utf8 -*-

import cv2
import threading
import serial
import time


ser = serial.Serial('/dev/serial0', 115200, timeout=1)
print('ser.name : ', ser.name)
## webcam 이미지 capture
cam = cv2.VideoCapture(0)
print('cam ok')
## 이미지 속성 변경 3 = width, 4 = height
cam.set(3, 320)
cam.set(4, 240)

## 0~100에서 90의 이미지 품질로 설정 (default = 95)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

global_dic = {'counter': False, 'sum_time': 0, 'try_num': 0}


def input_func():
    s1 = raw_input()
    if s1 == "s":
        global_dic['counter'] = True


def print_result(delay_time, faces):
    print('haar time : ', delay_time, "|| Faces : ", len(faces))
    if global_dic['counter']:
        global_dic['sum_time'] += delay_time
        global_dic['try_num'] += 1
        print('Try : ', global_dic['try_num'], '|| Average time : ', global_dic['sum_time'] / global_dic['try_num']
              , '|| haar time : ', delay_time, "|| Faces : ", len(faces))
    else:
        print('haar time : ', delay_time, "|| Faces : ", len(faces))


def haar(frame):
    list_size = 1
    global count
    global result
    start_time = time.time()
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if list_size == 1:
        if len(faces) != 0:
            result = "0314228071"
        else:
            result = "0314208071"

        ser.write(result.encode())
        delay_time = time.time() - start_time
        print_result(delay_time, faces)

    elif list_size > 1:
        if count == 0:
            if len(faces) != 0:
                result = "0314228071"
                count += 1
            else:
                result = "0314208071"
                count += 1

        if len(faces) != 0:
            if result == "0314228071":
                count += 1
            else:
                count = 0
        else:
            if result == "0314208071":
                count += 1
            else:
                count = 0

        if count == list_size:
            ser.write(result.encode())
            delay_time = time.time() - start_time
            # print('haar time : ', delay_time)
            print_result(delay_time, faces)
            count = 0


ret, frame = cam.read()
th_haar = threading.Thread()
count = 0
result = "0314218071"
while True:
    # 비디오의 한 프레임씩 읽는다.
    # 제대로 읽으면 ret = True, 실패면 ret = False, frame에는 읽은 프레임
    ret, frame = cam.read()
    if ret == False:
        print("cam read is failed")
        cam = cv2.VideoCapture(0)
        continue

    if th_haar != 0 or th_haar.is_alive() == False:
        th_haar = threading.Thread(target=haar, args=(frame,))
        th_haar.start()

cam.release()