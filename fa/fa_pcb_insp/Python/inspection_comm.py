#!/usr/bin/env  python3
# -*- coding: utf8 -*-
from enum import Enum
import socket
import random
import inspection_components
import json
import os
import sys

class SMT_ERROR(Enum) :
    PARTS_WRONG         = 0b0000000001        # No.1 오삽
    PARTS_NONE          = 0b0000000010        # No.2 미삽
    SOLDERING_NONE      = 0b0000000100        # No.3 미납
    SOLDERING_LITTLE    = 0b0000001000        # No.4 소납
    SOLDERING_OVER      = 0b0000010000        # No.5 과납
    MARKING             = 0b0000100000        # No.6 마킹
    CIRCUIT_SHORT       = 0b0001000000        # No.7 쇼트
    PARTS_CRACK         = 0b0010000000        # No.8 부품 crack
    SOLDERING_CRACK     = 0b0100000000        # No.9 납땜 crack
    PARTS_REVERSE       = 0b1000000000        # No.10 역삽

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 5843               # Arbitrary non-privileged port

# os.chdir("/home/pi/Desktop/")
print('')
print('    ┌───────────────────────────────┐')
print('    │\033[1;31m    INSPECTION SERVER START!\033[0m   │')
print('    └───────────────────────────────┘')
ic = inspection_components.inspection()

while True :
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('    ----------------------------------')
            print('    Connected by \033[1;32m', addr, '\033[0m')
            print('    ----------------------------------')

            while True:
                data = conn.recv(1024)
                if not data: break
                if len(data) > 0 :
                    decoded = data.decode()
                    splited = decoded.split(' ')
                    instruction = splited[0]

                    x1 = int(splited[1])
                    y1 = int(splited[2])
                    x2 = int(splited[3])
                    y2 = int(splited[4])

                    boardName = splited[5]
                    partsName = splited[6]

                    resultDictionary = {}

                    InspectList = int(splited[7])
                    dataPath = splited[8]

                    if instruction == 'Inspect' :
                        print('    \033[1;32m# Run Inspect function\033[0m')
                        if InspectList & SMT_ERROR.PARTS_WRONG.value :
                            # 1 . 오삽 처리 결과
                            resultDictionary[SMT_ERROR.PARTS_WRONG.name] = ic.parts_wrong(x1,y1,x2,y2,boardName,partsName,dataPath)
                            print('      └\033[1;33m', SMT_ERROR.PARTS_WRONG.name ,
                                    '\033[1;36m[',resultDictionary[SMT_ERROR.PARTS_WRONG.name][1],']\033[0m')

                        if InspectList & SMT_ERROR.PARTS_NONE.value :
                            # 2 . 미삽 처리 결과
                            resultDictionary[SMT_ERROR.PARTS_NONE.name] = ic.parts_none(x1,y1,x2,y2,boardName,partsName,dataPath)
                            print('      └\033[1;33m', SMT_ERROR.PARTS_NONE.name ,
                                    '\033[1;36m[',resultDictionary[SMT_ERROR.PARTS_NONE.name][1],']\033[0m')

                        if InspectList & SMT_ERROR.SOLDERING_NONE.value :
                            # 3 . 미납 처리 결과
                            resultDictionary[SMT_ERROR.SOLDERING_NONE.name] = False
                            print('      └\033[1;33m', SMT_ERROR.SOLDERING_NONE.name , 
                                    '\033[1;36m[',resultDictionary[SMT_ERROR.SOLDERING_NONE.name][1],']\033[0m')

                        if InspectList & SMT_ERROR.SOLDERING_LITTLE.value :
                            # 4 . 소납 처리 결과
                            resultDictionary[SMT_ERROR.SOLDERING_LITTLE.name] = False
                            print('      └\033[1;33m', SMT_ERROR.SOLDERING_LITTLE.name , 
                                    '\033[1;36m[',resultDictionary[SMT_ERROR.SOLDERING_LITTLE.name][1],']\033[0m')

                        if InspectList & SMT_ERROR.SOLDERING_OVER.value :
                            # 5 . 과납 처리 결과
                            resultDictionary[SMT_ERROR.SOLDERING_OVER.name] = False
                            print('      └\033[1;33m', SMT_ERROR.SOLDERING_OVER.name , 
                                    '\033[1;36m[',resultDictionary[SMT_ERROR.SOLDERING_OVER.name][1],']\033[0m')

                        if InspectList & SMT_ERROR.MARKING.value :
                            # 6 . 마킹 처리 결과
                            resultDictionary[SMT_ERROR.MARKING.name] = ic.parts_marking(x1,y1,x2,y2,boardName,partsName,dataPath)
                            print('      └\033[1;33m', SMT_ERROR.MARKING.name , 
                                    '\033[1;36m[',resultDictionary[SMT_ERROR.MARKING.name][1],']\033[0m')

                        if InspectList & SMT_ERROR.CIRCUIT_SHORT.value :
                            # 7 . 쇼트 처리 결과
                            resultDictionary[SMT_ERROR.CIRCUIT_SHORT.name] = False
                            print('      └\033[1;33m', SMT_ERROR.CIRCUIT_SHORT.name , 
                                    '\033[1;36m[',resultDictionary[SMT_ERROR.CIRCUIT_SHORT.name][1],']\033[0m')

                        if InspectList & SMT_ERROR.PARTS_CRACK.value :
                            # 8 . 부품 Crack 처리 결과
                            resultDictionary[SMT_ERROR.PARTS_CRACK.name] = False
                            print('      └\033[1;33m', SMT_ERROR.PARTS_CRACK.name , 
                                    '\033[1;36m[',resultDictionary[SMT_ERROR.PARTS_CRACK.name][1],']\033[0m')

                        if InspectList & SMT_ERROR.SOLDERING_CRACK.value :
                            # 9 . 납땜 Crack 처리 결과
                            resultDictionary[SMT_ERROR.SOLDERING_CRACK.name] = False
                            print('      └\033[1;33m', SMT_ERROR.SOLDERING_CRACK.name , 
                                    '\033[1;36m[',resultDictionary[SMT_ERROR.SOLDERING_CRACK.name][1],']\033[0m')

                        if InspectList & SMT_ERROR.PARTS_REVERSE.value :
                            # 10. 역삽 처리 결과
                            resultDictionary[SMT_ERROR.PARTS_REVERSE.name] = False
                            print('      └\033[1;33m', SMT_ERROR.PARTS_REVERSE.name , 
                                    '\033[1;36m[',resultDictionary[SMT_ERROR.PARTS_REVERSE.name][1],']\033[0m')

                        jsonParsed = json.dumps(resultDictionary)
                        conn.send(jsonParsed.encode())
                        print('    Done...\n')

                    elif instruction == 'LearnData' :
                        print('    \033[1;36m# Run learning data function\033[0m        ')
                        state =  1 if InspectList & SMT_ERROR.PARTS_WRONG.value else 0
                        state =  2 if InspectList & SMT_ERROR.PARTS_NONE.value else state
                        state =  3 if InspectList & SMT_ERROR.SOLDERING_NONE.value else state
                        state =  4 if InspectList & SMT_ERROR.SOLDERING_LITTLE.value else state
                        state =  5 if InspectList & SMT_ERROR.SOLDERING_OVER.value else state
                        state =  6 if InspectList & SMT_ERROR.MARKING.value else state
                        state =  7 if InspectList & SMT_ERROR.CIRCUIT_SHORT.value else state
                        state =  8 if InspectList & SMT_ERROR.PARTS_CRACK.value else state
                        state =  9 if InspectList & SMT_ERROR.SOLDERING_CRACK.value else state
                        state = 10 if InspectList & SMT_ERROR.PARTS_REVERSE.value else state
                        learnResult = ic.component_learn(x1,y1,x2,y2,boardName,partsName,state,dataPath)
                        learnResultString = '1' if learnResult is True else '0'
                        conn.send(learnResultString.encode())
                        print('    Done...\n')
                    else :
                        print('!!!! Unknown function input\n\n\n')
