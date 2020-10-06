# FaceRecg  

- compile
```
FaceRecg/src $ make && ./app.out
```

### serial 통신 연결
- 라즈베리파이 serial 활성화
```
$ sudo raspi-config
```
Serial enable 선택  
```
$ sudo reboot
```

- 시리얼 통신을 위한 장치 파일 /dev/ttyS0 생성
```
$ ls /dev/tty* -al
```
 디바이스 파일 /dev/ttyS0 추가 생성 된 것 확인  
(기타 설정 : http://cms3.koreatech.ac.kr/sites/joo/IFC415/IFC415_08.pdf)

- serial 통신 연결 확인
```
$ stty -F /dev/ttyAMA0 115200
$ echo -e "hello world\r\n" > /dev/ttyAMA0
```
- WiringPi 
```
$ git clone https://github.com/WiringPi/WiringPi.git
$ cd WiringPi
$ ./build
```

- puTTY로 접속
serial 선택 후 시리얼 포트(장치관리자에서 확인), baud rate 입력( ex. COM6, 115200)

