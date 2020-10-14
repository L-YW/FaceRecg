#!/usr/bin/env python
# -*- coding: utf8 -*-


import socket
import cv2
import numpy as np
import socket

class Server:
    # socket에서 수신한 버퍼를 반환하는 함수
    def recvall(self, sock, count):
        # 바이트 문자열
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def recvall_main(self):
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

        while True:
            # client에서 받은 stringData의 크기 (==(str(len(stringData))).encode().ljust(16))
            length = self.recvall(conn, 16)
            stringData = self.recvall(conn, int(length))
            data = np.fromstring(stringData, dtype='uint8')

            # data를 디코딩한다.
            self.frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
            self.haar()
            cv2.imshow('ImageWindow', self.frame)
            cv2.waitKey(1)

    def haar(self):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(self.frame, (x, y), (x+w, y+h), (255, 0, 0), 2)            