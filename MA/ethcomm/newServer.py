#!/usr/bin/env python
# -*- coding: utf8 -*-


import socket
import cv2
import numpy as np
import socket
import hud
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject
import cv2


class Listener(QObject):
    index = 0
    user_signal = pyqtSignal(np.ndarray, int)

    def getMessageFromUser(self, rectFrame, faceResult):
        self.user_signal.emit(rectFrame, faceResult)


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
        self.listener.user_signal.connect(self.img_rander)

        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 800, 460)
        hbox = QHBoxLayout()
        hbox.addWidget(self.label_navi)
        hbox.addWidget(self.label_rand)
        hbox.addWidget(self.label_state)
        self.setLayout(hbox)

    @pyqtSlot(np.ndarray, int)
    def img_rander(self, rectFrame, faceResult):
        h, w, c = rectFrame.shape
        qImg = QImage(rectFrame.data, w, h, w * c, QImage.Format_RGB888)
        img_vi = QPixmap.fromImage(qImg)
        self.label_rand.setPixmap(img_vi)
        print("drowsy_result : ", faceResult)
        if faceResult == 1:  # 정면일때
            print('11')
            self.pixmap_state = QPixmap(".//img//normal.jpg")
        elif faceResult == 2:  # 정면이 아닐때
            print('22')
            self.pixmap_state = QPixmap(".//img//warning.jpg")
        self.label_state.setPixmap(self.pixmap_state)

    # 메세지를 받았을 때
    def getMsg(self, rectFrame, faceResult):
        self.listener.getMessageFromUser(rectFrame, faceResult)


# socket에서 수신한 버퍼를 반환하는 함수
def recvall(sock, count):
    # 바이트 문자열
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def haar(frame):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    if len(faces) != 0:
        result = 1
    else:
        result = 2
    return result, frame


def myThread():
    while True:
        # client에서 받은 stringData의 크기 (==(str(len(stringData))).encode().ljust(16))
        length = recvall(conn, 16)
        stringData = recvall(conn, int(length))
        data = np.fromstring(stringData, dtype='uint8')

        # data를 디코딩한다.
        frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
        faceResult, rectFrame = haar(frame)
        form.getMsg(rectFrame, faceResult)


HOST = ''
PORT = 8485

# TCP 사용
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

# 서버의 아이피와 포트번호 지정
s.bind((HOST, PORT))
print('Socket bind complete')
# 클라이언트의 접속을 기다린다. (클라이언트 연결을 10개까지 받는다)
s.listen(10)
print('Socket now listening')

# 연결, conn에는 소켓 객체, addr은 소켓에 바인드 된 주소
conn, addr = s.accept()

import sys

app = QApplication([])
form = Window()
form.show()

th = threading.Thread(target=myThread)
th.start()

app.exec_()
