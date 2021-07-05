import serial

ser = serial.Serial('/dev/ttyAMA0', 115200)
ser.open()
answer = ser.readline()
ser.close()
print(answer)
