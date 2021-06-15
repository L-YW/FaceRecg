import os
from turtle import pd
import json
import inspection
import cv2
import calcMissing as hist

ic = inspection.inspection()
file_path = input('경로 입력 : ')

def importDataset():
    f2 = open('C:\\python', 'r')
    data = []
    while True:
        line = f2.readline()
        if not line:break
        data.append(line)
    return data

def learnFeatures(b_name, p_name, jpec_data):
    # 디렉토리가 있는지 확인 한 후 보드 디렉토리 생성
    try:
        if os.path.isdir(file_path) is False:
            print("try to check dir")
    except OSError as e:
        print("OS error: {0}".format(e))
        print("\033[1;33m      [Make directory error]\033[0m")
        print("\033[1;31m      The board directory cannot be created in the path.\033[0m")
        return False

    # Crop한 이미지를 저장. 문제시 False 리턴
    try:
        img = cv2.imread(file_path)
        category = 1
        while(1):
            cv2.imwrite('./' + b_name + '/' + p_name + '_' + category + '.jpg', img)
            category += 1
            if category is 256:
                break

    except:
        print("\033[1;33m      [Write file error]\033[0m")
        print("\033[1;31m      The parts sub image cannot be write in the path.\033[0m")
        return False
    return True

"""=========================================================================================================================
    검사 함수 | 이미지를 비교하여 color 알고리즘으로 검사하는 함수. 
========================================================================================================================="""

def DoInspection(b_name, p_name):
    img_good = cv2.imread('./' + b_name + '/' + p_name + '_' + '0' + '.jpg')
    img_insp = cv2.imread(file_path)

    # 검사 및 정상 이미지가 잘 로드 되었는지 확인하는 부분
    if check_imread(img_good, "Normal image") is False:
        return [str(False), str(0)]
    if check_imread(img_insp, "Inspection image") is False:
        return [str(False), str(0)]

    # 검사 및 정상 이미지가 10kb가 넘는지 확인하는 부분
    if check_file_over_10kb('./' + b_name + '/' + p_name + '_' + '0' + '.jpg', "Normal image") is False:
        return [str(False), str(0)]
    if check_file_over_10kb(file_path, "Inspection image") is False:
        return [str(False), str(0)]

    # =====================================================================================================================
    #  정상이미지와 검사 이미지의 corr1 값 구하기
    # =====================================================================================================================
    img_insp = img_insp[y1:y2, x1:x2]
    start = cv2.getTickCount()
    corr1 = hist.HistCompareMissing_Equalized(img_good, img_insp)
    end = cv2.getTickCount()
    time_good = (end - start) / cv2.getTickFrequency()

    # 불량 이미지 로드
    learningPath = './' + b_name + '/' + p_name + '_' + str(state) + '.jpg'
    img_learn = cv2.imread(learningPath)
    if check_file_over_10kb(learningPath, "Learning image") is False:
        return [str(False), str(0)]

    # =====================================================================================================================
    #  불량 이미지가 학습 되어있을 경우, 불량 이미지와 검사 이미지의 corr2값을 구함
    # =====================================================================================================================
    if img_learn is not None:
        start = cv2.getTickCount()
        corr2 = hist.HistCompareMissing_Equalized(img_learn, img_insp)
        end = cv2.getTickCount()
        time_insp = (end - start) / cv2.getTickFrequency()
        time = time_good + time_insp

        print('      ', corr1, ' , ', corr2)
        # corr1 (vs 정상) 과 corr2 (vs 불량)의 대소 비교
        result_inspection = True if corr1 > corr2 else False

    # =====================================================================================================================
    #  불량 이미지가 학습되어 있지 않을 경우, corr1이 Threshold 값을 넘는지 확인
    # =====================================================================================================================
    else:
        result_inspection = True if corr1 > 0.7 else False
    return [str(result_inspection), str(random.uniform(0.30, 0.38))]

"""=========================================================================================================================
    이미지가 정상적으로 열렸는지 확인하는 함수
========================================================================================================================="""

def check_imread(img, fileType):
    if img is None:
        print("\033[1;33m      [Image load fialed error]\033[0m")
        print("\033[1;31m      " + fileType + " load failed\033[0m")
        return False
    return True

"""=========================================================================================================================
    주어진 경로의 파일이 10kb가 넘는지 확인하는 함수
========================================================================================================================="""

def check_file_over_10kb(filepath, fileType):
    if os.path.exists(filepath) and os.path.getsize(filepath) < 512:  # bytes
        print("\033[1;33m      [Corrupted image file error]\033[0m")
        print("\033[1;31m      " + fileType + " size is not over 10kb\033[0m")
        return False
    return True



def componentName():
    f3 = open('C:\\python\\componentName.json', 'r')
    return 0

def importDataset():
    print(file_path)
    file_list = os.listdir(file_path)
    file_list_jpeg = [file for file in file_list if file.endswith('.jpeg')]
    fileName: str
    for fileName in file_list_jpeg:
        print(fileName)

def jpegConcat(file_list):
    # jpeg 파일들을 DataFrame으로 불러와서 concat
    df = pd.DataFrame()
    for i in file_list:
        data = pd.read_jpeg(file_path + i)
        df = pd.concat([df, data])
    df.df.reset_index(drop=True)

def loadJson(file_list):
    # json 파일들을 DataFrame으로 불러오기
    dict_list = []
    for i in file_list:
        for line in open((file_path + i), "r"):
            dict_list.append(json.loads(line))
    df = pd.DataFrame(dict_list)

def saveJson():
    json_path = "./sample.json"
    data={}
    data[''] = []
    data['posts'].append({

    })
    print(data)

    with open(json_path, "w") as outfile:
        json.dump(data, outfile)

file_txt = 'C:\\python\\cropRange.txt'
learn_or_inspection = input('please enter 1(learn) or 2(inspection) : ')
file_path = input('경로 입력 : ')
if os.path.isfile(file_txt):
    x1, y1, x2, y2 = loadCropRange()
else:
    saveCropRange()

loadDataset()
learnFeatures()
DoInspection()
saveJson()

import json

with open('json file path or name') as json_file:
    json_data = json.load(json_file)

for i in range(0, range):
    json_data['algorithm']['hist'][i]['N/E']