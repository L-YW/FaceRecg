#!/usr/bin/env  python3
# -*- coding: utf8 -*-
import socket
import random

def inspection_cmd(str_cmd) :
	return random.randrange(0,2)

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 5843               # Arbitrary non-privileged port

while True :
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data: break
                if len(data) > 0 :
                    print(data.decode())
                    result = inspection_cmd(data.decode())
                    print(result)
                    conn.send(str(result).encode())
