import os
from turtle import pd

from PyQt5.QtWidgets import QFileDialog
path = './path'

def showDialog2():
    print(path)
    file_list = os.listdir(path)
    file_list_py = [file for file in file_list if file.endswith('.jpeg')]

def jpegConcat(file_list_py):
    # jpeg 파일들을 DataFrame으로 불러와서 concat
    df = pd.DataFrame()
    for i in file_list_py:
        data = pd.read_jpeg(path + i)
        df = pd.concat([df, data])
    df.df.reset_index(drop=True)

def loadJson(file_list_py):
    # json 파일들을 DataFrame으로 불러오기
    import json
    dict_list = []
    for i in file_list_py:
        for line in open((path + i), "r"):
            dict_list.append(json.loads(line))
    df = pd.DataFrame(dict_list)