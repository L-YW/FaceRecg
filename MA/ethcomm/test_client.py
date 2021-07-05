import serial

ser = serial.Serial('/dev/serial1', 115200)
string = "031420871"
ser.open()
ser.write(bytes(string.encode()))
ser.close()