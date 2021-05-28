import os
from turtle import pd

from PyQt5.QtWidgets import QFileDialog
path = input('경로 입력 : ')

def loadDataset():
    print(path)
    file_list = os.listdir(path)
    file_list_jpeg = [file for file in file_list if file.endswith('.jpeg')]
    fileName: str
    for fileName in file_list_jpeg:
        print(fileName)

def jpegConcat(file_list):
    # jpeg 파일들을 DataFrame으로 불러와서 concat
    df = pd.DataFrame()
    for i in file_list:
        data = pd.read_jpeg(path + i)
        df = pd.concat([df, data])
    df.df.reset_index(drop=True)

def loadJson(file_list):
    # json 파일들을 DataFrame으로 불러오기
    import json
    dict_list = []
    for i in file_list:
        for line in open((path + i), "r"):
            dict_list.append(json.loads(line))
    df = pd.DataFrame(dict_list)


loadDataset()