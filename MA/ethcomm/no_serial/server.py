#!/usr/bin/env python
# -*- coding: utf8 -*-

# =====================================================================================================
#  Import
# =====================================================================================================
import cv2, socket, threading
import numpy as np
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject

# =====================================================================================================
#  Signal을 듣는 Class
# =====================================================================================================
class Listener(QObject):
    # sig1 : 사진 변경 / sig2 : 얼굴 아이콘 변경
    user_signal1 = pyqtSignal(np.ndarray)
    user_signal2 = pyqtSignal(bytes)

    # 이미지 전달 받음
    def getMessageFromUser1(self, rectFrame):
        self.user_signal1.emit(rectFrame)

    # 얼굴 판독 결과와 Rect 좌표 받음
    def getMessageFromUser2(self, string):
        self.user_signal2.emit(string)

# =====================================================================================================
#  PyQT 윈도우
# =====================================================================================================
class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        background_image = QImage(".//img//background.JPG")
        palette = QPalette()
        palette.setBrush(10, QBrush(background_image))
        self.setPalette(palette)

        # 얼굴 Rect와 그 color
        self.faceRect = [0,0,0,0]
        self.color = (0,255,0)

        self.label_navi = QLabel()
        self.label_rand = QLabel()
        self.label_state = QLabel()
        self.pixmap_navi = QPixmap(".//img//left_image.JPG")
        self.pixmap_rand = QPixmap(".//img//white.jpg")
        self.pixmap_state = QPixmap(".//img//warning.jpg")
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

    # =================================================================================================
    #  카메라로 부터 단순 이미지를 수신 했을 때
    # =================================================================================================
    @pyqtSlot(np.ndarray)
    def img_rander(self, rectFrame):
        rectFrame = cv2.cvtColor(rectFrame, cv2.COLOR_BGR2RGB)
        # 얼굴 영역 그려주기
        rectFrame = cv2.rectangle(rectFrame,(self.faceRect[0],self.faceRect[1]),
                                  (self.faceRect[2],self.faceRect[3]),self.color,2)
        h, w, c = rectFrame.shape
        qImg = QImage(rectFrame.data, w, h, w * c, QImage.Format_RGB888)
        img_vi = QPixmap.fromImage(qImg)
        self.label_rand.setPixmap(img_vi)

    # =================================================================================================
    #  정면 판독 결과를 수신 했을 때
    # =================================================================================================
    @pyqtSlot(bytes)
    def drowsy_result(self, string):
        inputStr = string.decode('utf-8')   # 받은 bytes를 str로 변환
        faceResult = inputStr.split(',')    # "판독 결과,x,y,w,h" 를 ,로 split (client.py:53 참고)
        print(inputStr[0])                  # Debug용 출력
        if faceResult[0] == "0314228071":   # 정면일때
            self.pixmap_state = QPixmap(".//img//normal.jpg")
            self.faceRect = [int(faceResult[1]),int(faceResult[2]),
                             int(faceResult[1])+int(faceResult[3]),
                             int(faceResult[2])+int(faceResult[4])]
            # faceRect에 [x, y, x+w, y+h] 반영
            self.color = (0, 255, 0)         # 찾으면 초록색 네모로
        elif faceResult[0] == "0314208071":  # 정면이 아닐때
            self.pixmap_state = QPixmap(".//img//warning.jpg")
            # self.faceRect = [0,0,0,0]
            self.color = (255,0,0)           # 못 찾으면 빨간 네모로
        self.label_state.setPixmap(self.pixmap_state)
        # 이미지 업데이트

    # =================================================================================================
    # 메세지를 받았을 때
    # =================================================================================================
    def getMsg1(self, rectFrame):
        self.listener.getMessageFromUser1(rectFrame)
    def getMsg2(self,string):
        self.listener.getMessageFromUser2(string)



# =====================================================================================================
#  ★ Global 영역 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# =====================================================================================================
#  socket에서 수신한 버퍼를 반환하는 함수
# =====================================================================================================
def recvall(sock, count):
    # 바이트 문자열
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

# =====================================================================================================
#  Socket으로부터 이미지를 받아오는 스레드 (8485 포트 사용)
# =====================================================================================================
def myThread():
    while True:
        # client에서 받은 stringData의 크기 (==(str(len(stringData))).encode().ljust(16))
        length = recvall(conn, 16)
        stringData = recvall(conn, int(length))
        data = np.fromstring(stringData, dtype='uint8')

        # data를 디코딩한다.
        frame = cv2.imdecode(data, cv2.IMREAD_UNCHANGED )
        form.getMsg1(frame)

# =====================================================================================================
#  Socket으로부터 정면 판독 결과와 얼굴 영역을 받아오는 스레드 (8486 포트 사용)
# =====================================================================================================
def myThread2():
    while True:
        faceResult = recvall(conn2, 32)     # 넉넉하게 32글자 읽어옴 (client.py:59 참조)
        form.getMsg2(faceResult)

# =====================================================================================================
#  Main Session
# =====================================================================================================
HOST = ''           # 호스트
PORT = 8485         # 이미지를 받아올 소켓의 포트
PORT2 = 8486        # 판독

# ★ 이미지를 가져오는 포트를 열기
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

# ★ 결과를 가져오는 포트를 열기
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket2 created')
s2.bind((HOST, PORT2))
print('Socket2 bind complete')
s2.listen(10)
print('Socket2 now listening')
conn2, addr2 = s2.accept()

app = QApplication([])
form = Window()
form.show()

# 이미지 가져오는 스레드 시작
th = threading.Thread(target=myThread)
th.start()

# 결과 가져오는 스레드 시작
th2 = threading.Thread(target=myThread2)
th2.start()

app.exec_()