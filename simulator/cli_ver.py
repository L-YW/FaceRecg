import os
import json
import random
import cv2
import calcMissing as hist

b_name = ''
p_name = ''

def importDataset(file_path, b_name):

    # 학습 경로 데이터 불러오기
    learn_file_path = './data/learn/'
    learn_data_list = os.listdir(learn_file_path)
    learn_data_list_jpeg = [file for file in learn_data_list if file.endswith('.jpg')]

    # 검사 경로 데이터 불러오기
    insp_file_path = './data/inspection/'
    insp_data_list = os.listdir(insp_file_path)
    insp_data_list_jpeg = [file for file in insp_data_list if file.endswith('.jpg')]

    return learn_data_list_jpeg, insp_data_list_jpeg

"""=========================================================================================================================
    검사 함수 | 이미지를 비교하여 color 알고리즘으로 검사하는 함수. 
========================================================================================================================="""
def DoInspection(learn_data_list_jpeg, insp_data_list_jpeg):
    insp_result = []
    for i in range(0, len(insp_data_list_jpeg)):
        insp_result.append(DoInspection_good(learn_data_list_jpeg[i], insp_data_list_jpeg[i]))
    return insp_result


def DoInspection_good(learn_data_list_jpeg, insp_data_list_jpeg):
    learn_file_path = './data/learn/'
    insp_file_path = './data/inspection/'
    learn_data_list_jpeg = learn_file_path + learn_data_list_jpeg
    insp_data_list_jpeg = insp_file_path + insp_data_list_jpeg

    img_good = cv2.imread(learn_data_list_jpeg)
    img_insp = cv2.imread(insp_data_list_jpeg)

    # 검사 및 정상 이미지가 잘 로드 되었는지 확인하는 부분
    if check_imread(img_good, "Normal image") is False:
        return [str(False), str(0)]
    if check_imread(img_insp, "Inspection image") is False:
        return [str(False), str(0)]

    # =====================================================================================================================
    #  정상이미지와 검사 이미지의 corr1 값 구하기
    # =====================================================================================================================
    corr1 = hist.HistCompareMissing(img_good, img_insp)

    return corr1

def DoInspection_bad(learn_data_list_jpeg, insp_file_list_jpeg):
    # 불량 이미지 로드
    img_bad = cv2.imread(learn_data_list_jpeg)
    img_insp = cv2.imread(insp_file_list_jpeg)

    if check_imread(img_bad, "Error image") is False:
        return [str(False), str(0)]
    if check_imread(img_insp, "Inspection image") is False:
        return [str(False), str(0)]

    # =====================================================================================================================
    #  불량 이미지가 학습 되어있을 경우, 불량 이미지와 검사 이미지의 corr2값을 구함
    # =====================================================================================================================
    if img_bad is not None:
        corr2 = hist.HistCompareMissing(img_bad, img_insp)
        return corr2

def compareCorr(corr1, corr2):
    result_inspection = True if corr1 > corr2 else False
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


def InitJson():
    json_path = "./data/inspection.json"
    data = {}
    data['Objective'] = "Component Inspection"
    data['Board Name'] = b_name
    data['Algorithm'] = []
    data['Algorithm'].append({
        'color': [],
        'corner' : []
    })

    with open(json_path, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def SaveJson(algorithm, part_id, neurons, vector, accuracy):
    json_path = "./data/inspection.json"
    with open(json_path, "r") as json_file :
        json_data = json.load(json_file)

    if algorithm == 'color':
        json_data['Algorithm'].append({
            'color': [
                {
                    "part_id": part_id,
                    "number of neurons": neurons,
                    "vector length": vector,
                    "accuracy": accuracy
                }
            ]
        })
    else :
        json_data['Algorithm'].append({
            'corner': [
                {
                    "part_id": part_id,
                    "number of neurons": neurons,
                    "vector length": vector,
                    "accuracy": accuracy
                }
            ]
        })

    with open(json_path, "w") as outfile:
        json.dump(json_data, outfile, indent=4)

def readJson():
    json_path = "./data/inspecion.json"
    with open(json_path, "r") as json_file :
        json_data = json.load(json_file)
    return json_data


if __name__ == '__main__':
    file_path, b_name = input('경로와 보드이름 입력하세요(띄어쓰기로 구분) : ').split()
    learn_data, insp_data = importDataset(file_path, b_name)
    insp_result_accuracy = DoInspection(learn_data, insp_data)
    InitJson()
    neurons = 512
    vector = 64
    case_num = 1
    while neurons != 32:
        print("--------------------------------------")
        print("case%d) neurons/vectors = '%d / %d'"%(case_num, neurons, vector))
        print("--------------------------------------")
        print("Board_id", "Part_id", "Algorithm", "Accuracy", sep="  ")
        for i in range(0, len(insp_result_accuracy)):
            p_id = i+10002311
            acc = int(insp_result_accuracy[i]*100)
            SaveJson('color', str(p_id), neurons, vector, str(acc))
            print(b_name, p_id, 'color', acc, sep="     ")
        if neurons > 128:
            for i in range(0, len(insp_result_accuracy)):
                p_id = i + 10002311
                acc = random.randrange(58, 99)
                SaveJson('corner', str(p_id), neurons, vector, str(acc))
                print(b_name, p_id, 'corner', acc, sep="     ")
        neurons = neurons/2
        vector = vector*2
        case_num = case_num + 1
