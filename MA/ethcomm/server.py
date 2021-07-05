#!/usr/bin/env python3
# -*- coding: utf8 -*-


import socket
import cv2
import numpy as np
import socket
import threading
import serial
import binascii
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject

class Listener(QObject):
    user_signal1 = pyqtSignal(np.ndarray)
    user_signal2 = pyqtSignal(str)

    def getMessageFromUser1(self, rectFrame):
        self.user_signal1.emit(rectFrame)

    def getMessageFromUser2(self,string):
        self.user_signal2.emit(string)

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        background_image = QImage(".//img//background.JPG")
        palette = QPalette()
        palette.setBrush(10, QBrush(background_image))
        self.setPalette(palette)

        self.label_navi = QLabel()
        self.label_rand = QLabel()
        self.label_state = QLabel()
        self.pixmap_navi = QPixmap(".//img//left_image.JPG")
        self.pixmap_rand = QPixmap(".//img//white.jpg")
        self.pixmap_state = QPixmap(".//img//normal.jpg")
        self.label_navi.setPixmap(self.pixmap_navi)
        self.label_rand.setPixmap(self.pixmap_rand)
        self.label_state.setPixmap(self.pixmap_state)

        self.listener = Listener()
        self.listener.user_signal1.connect(self.img_rander)
        self.listener.user_signal2.connect(self.drowsy_result)

        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 800, 460)
        hbox = QHBoxLayout()
        hbox.addWidget(self.label_navi)
        hbox.addWidget(self.label_rand)
        hbox.addWidget(self.label_state)
        self.setLayout(hbox)


    @pyqtSlot(np.ndarray)    
    def img_rander(self, rectFrame):               
        h, w, c = rectFrame.shape
        rectFrame = cv2.cvtColor(rectFrame, cv2.COLOR_BGR2RGB)
        qImg = QImage(rectFrame.data, w, h, w * c, QImage.Format_RGB888)
        qImg = qImg.scaledToWidth(200)
        img_vi = QPixmap.fromImage(qImg)
        self.label_rand.setPixmap(img_vi)
        
    
    @pyqtSlot(str)
    def drowsy_result(self, b_face):
        print("debug",b_face)  
        if b_face :  # 정면일때
            self.pixmap_state = QPixmap(".//img//normal.jpg")
        else :  # 정면이 아닐때
            self.pixmap_state = QPixmap(".//img//warning.jpg")
        self.label_state.setPixmap(self.pixmap_state)
        

    # 메세지를 받았을 때
    def getMsg1(self, rectFrame):
        self.listener.getMessageFromUser1(rectFrame)

    def getMsg2(self):
        self.listener.getMessageFromUser2()


#socket에서 수신한 버퍼를 반환하는 함수
def recvall(sock, count):
    # 바이트 문자열
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def myThread():    
    while True:
        # client에서 받은 stringData의 크기 (==(str(len(stringData))).encode().ljust(16))
        length = recvall(conn, 16)
        stringData = recvall(conn, int(length))
        data = np.fromstring(stringData, dtype = 'uint8')
        
        # data를 디코딩한다.
        frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
        form.getMsg1(frame)

def myThread2():
    #serial port : serial pins(5V, G, TX, RX) must be connected
    ser=serial.Serial('/dev/serial0', 9600, timeout=1)
    recv_str = str()
    face_history = list()
    list_size = 5
    for i in range(0, list_size) :
        face_history.append(0)
    
    while True :
        try :
            print('starting read')
            recv_byte = ser.read()
            print('decoding')
            recv_str += recv_byte.decode()
            print('end read')
        except :
            print('Decode Exception')
            recv_str = ""
            continue
        print(recv_str) #debug print : remove this line after test it

        if recv_str.find("404") >= 0 :
            print('Found Face') # call green smile function
            recv_str = ""
            face_history.pop()
            face_history.insert(0,1)
        
        if recv_str.find("424") >= 0 :
            print('Not Found Face') # call red smile function
            recv_str = ""
            face_history.pop()
            face_history.insert(0,0)

        if face_history.count(1) == list_size :
            form.drowsy_result(True)
    
        if face_history.count(0) == list_size :
            form.drowsy_result(False)

        if len(recv_str) > 20 :
            recv_str = ""



    print('myThread2 is finished')


HOST=''
PORT=8485
 
#TCP 사용
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')
 
#서버의 아이피와 포트번호 지정
s.bind((HOST,PORT))
print('Socket bind complete')
# 클라이언트의 접속을 기다린다. (클라이언트 연결을 10개까지 받는다)
s.listen(10)
print('Socket now listening')
 
#연결, conn에는 소켓 객체, addr은 소켓에 바인드 된 주소
conn,addr=s.accept()

app = QApplication([])
form = Window()
form.show() 

th = threading.Thread(target=myThread)
th.start()

th2 = threading.Thread(target=myThread2)
th2.start()

app.exec_()
