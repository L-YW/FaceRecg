import serial
import time

#ser=serial.Serial('/dev/ttyS0', 9600, timeout=5, rtscts=1, xonxoff = 1)

#ser.parity = serial.PARITY_EVEN
#print(ser)
recv_str= str()
ser=serial.Serial('/dev/serial0', 9600, timeout=3)
while True:
    
    #time.sleep(2)
    print("read start") #debug print : remove this line after test it
    recv_str = ser.read(4)
    print(len(recv_str))
    try :
        print(recv_str.decode())
    except :
        continue
    print("read finish") #debug print : remove this line after test it
    #ser.flush()

ser.close()