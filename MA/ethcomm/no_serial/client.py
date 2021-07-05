#!/usr/bin/env python
# -*- coding: utf8 -*-

# =====================================================================================================
#  Import
# =====================================================================================================
import cv2, socket, numpy, argparse, threading

# =====================================================================================================
#  ★ 하르 진행 후 결과 전송하는 스레드
# =====================================================================================================
def haar():
    global frame        # global 변수 frame을 읽어옴
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    while True:
        cv2.waitKey(100)  # 이 값을 조절하여 원하는 딜레이 발생 가능
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.9, 3)

        # 찾은 얼굴의 좌표를 저장하는 변수
        rectData = [0, 0, 0, 0]
        if len(faces) != 0:  # SUCCESS !
            result = "0314228071"
            rectData = [faces[0][0], faces[0][1], faces[0][2], faces[0][3]]
            # 성공시 Face 좌표 x,y,w,h 전송
        else:  # FAIL !
            result = "0314208071"
            # 실패시 Face좌표 대신 0,0,0,0 전송

        # 얼굴 검사 결과,x,y,w,h 전송
        result = result \
                 + "," + str(rectData[0]) \
                 + "," + str(rectData[1]) \
                 + "," + str(rectData[2]) \
                 + "," + str(rectData[3])
        # 넉넉하게 32 글자 전송
        s2.sendall(result.encode().ljust(32))


# =====================================================================================================
#  Main Session
# =====================================================================================================

# 서버와 연결
parser = argparse.ArgumentParser(description='Sending data to server -i host ')
parser.add_argument('-i', help="host_ip", required=False, default='127.0.0.1')
args = parser.parse_args()
ip_str = args.i

print('server IP is : ' + ip_str)

## TCP 사용 ( s: 이미지 / s1 : 정면 판독 결과 )
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
## 이미지 전송에 사용할 포트
s.connect((ip_str, 8485))
## 정면 판독 결과 전송에 사용할 포트
s2.connect((ip_str, 8486))

# =====================================================================================================
#  카메라 세팅
# =====================================================================================================
## webcam 이미지 capture
cam = cv2.VideoCapture(0)
## 이미지 속성 변경 3 = width, 4 = height
cam.set(3, 320)
cam.set(4, 240)
## 0~100에서 90의 이미지 품질로 설정 (default = 95)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

ret, frame = cam.read()                     # 카메라 읽어오기
th_haar = threading.Thread(target=haar)     # 하르 스레드 시작
th_haar.start()

# =====================================================================================================
#  카메라 데이터는 전달하면서, global 변수 frame은 업데이트하는 loop문
# =====================================================================================================
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

    # 서버에 데이터 전송
    s.sendall((str(len(stringData))).encode().ljust(16) + stringData)

cam.release()



