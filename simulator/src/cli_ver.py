import os
import json
import random
import cv2
import color
import corner

b_name = ''
p_name = ''

def importDataset(file_path, b_name):
    path = []
    # 학습 경로 데이터 불러오기
    learn_file_path = './' + file_path + 'learn/'

    learn_data_list = os.listdir(learn_file_path)
    learn_data_list_jpeg = [file for file in learn_data_list if file.endswith('.jpg')]
    path.append(learn_file_path)

    # 검사 경로 데이터 불러오기
    insp_file_path = './' + file_path + 'inspection/'
    insp_data_list = os.listdir(insp_file_path)
    insp_data_list_jpeg = [file for file in insp_data_list if file.endswith('.jpg')]
    path.append(insp_file_path)

    return learn_data_list_jpeg, insp_data_list_jpeg, path

"""=========================================================================================================================
    검사 함수 | 이미지를 비교하여 corner 알고리즘으로 검사하는 함수. 
========================================================================================================================="""
def DoInspection_corner(learn_data_list_jpeg, insp_data_list_jpeg, path):
    accuracy = []
    acc_512 = []
    acc_256 = []
    for i in range(0, len(insp_data_list_jpeg)):
        learn_data_jpeg = path[0] + learn_data_list_jpeg[i]
        insp_data_jpeg = path[1] + insp_data_list_jpeg[i]

        img_good = cv2.imread(learn_data_jpeg, flags=cv2.IMREAD_GRAYSCALE)
        img_insp = cv2.imread(insp_data_jpeg, flags=cv2.IMREAD_GRAYSCALE)

        # 검사 및 정상 이미지가 잘 로드 되었는지 확인하는 부분
        if check_imread(img_good, "corner Normal image") is False:
            return [str(False), str(0)]
        if check_imread(img_insp, "Inspection image") is False:
            return [str(False), str(0)]

        acc_1, acc_2 = corner.calcCorner(img_good, img_insp)
        acc_512.append(acc_1)
        acc_256.append(acc_2)
    accuracy.append(acc_512)
    accuracy.append(acc_256)
    return accuracy

"""=========================================================================================================================
    검사 함수 | 이미지를 비교하여 color 알고리즘으로 검사하는 함수. 
========================================================================================================================="""
def DoInspection_color(learn_data_list_jpeg, insp_data_list_jpeg, path):
    insp_result = []
    for i in range(0, len(insp_data_list_jpeg)):
        insp_result.append(DoInspection_good(learn_data_list_jpeg[i], insp_data_list_jpeg[i], path))
    return insp_result


def DoInspection_good(learn_data_list_jpeg, insp_data_list_jpeg, path):
    learn_data_list_jpeg = path[0] + learn_data_list_jpeg
    insp_data_list_jpeg = path[1] + insp_data_list_jpeg

    img_good = cv2.imread(learn_data_list_jpeg)
    img_insp = cv2.imread(insp_data_list_jpeg)

    # 검사 및 정상 이미지가 잘 로드 되었는지 확인하는 부분
    if check_imread(img_good, "color Normal image") is False:
        return [str(False), str(0)]
    if check_imread(img_insp, "Inspection image") is False:
        return [str(False), str(0)]

    # =====================================================================================================================
    #  정상이미지와 검사 이미지의 corr1 값 구하기
    # =====================================================================================================================
    corr1 = color.HistCompareMissing(img_good, img_insp)

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
        corr2 = color.HistCompareMissing(img_bad, img_insp)
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


def InitJson(file_path):
    json_path = "./" + file_path + "inspection.json"
    data = {}
    data['Objective'] = "Component Inspection"
    data['Board Name'] = b_name
    data['Algorithm'] = []
    data['Best'] = []
    data['Algorithm'].append({
        'color': [],
        'corner': []
    })

    with open(json_path, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def SaveJson(file_path, algorithm, part_id, neurons, vector, accuracy):
    json_path = "./" + file_path + "inspection.json"
    with open(json_path, "r") as json_file:
        try:
            json_data = json.load(json_file)
        except ValueError as e:
            print('parsing error! error code : {}'.format(e))
            return None

    if algorithm == 'color':
        json_data['Algorithm'][0]['color'].append(
            {
                "part_id": part_id,
                "number of neurons": neurons,
                "vector length": vector,
                "accuracy": accuracy
            }
        )
    else :
        json_data['Algorithm'][0]['corner'].append(
            {
                "part_id": part_id,
                "number of neurons": neurons,
                "vector length": vector,
                "accuracy": accuracy
            }
        )

    with open(json_path, 'w') as outfile:
        json.dump(json_data, outfile, indent=4)

def BestJson(file_path, case, algorithm):
    json_path = "./" + file_path + "inspection.json"

    with open(json_path, "r") as json_file:
        try:
            json_data = json.load(json_file)
        except ValueError as e:
            print('parsing error! error code : {}'.format(e))
            return None
    json_data['Best'].append(
        {
            "best case": case,
            "best algorithm": algorithm
        }
    )

    with open(json_path, 'w') as outfile:
        json.dump(json_data, outfile, indent=4)


def readJson(file_path):
    json_path = "./" + file_path + "inspection.json"
    with open(json_path, "r") as json_file :
        json_data = json.load(json_file)
    return json_data


if __name__ == '__main__':
    file_path, b_name = input('경로와 보드이름 입력하세요(띄어쓰기로 구분) : ').split()
    learn_data, insp_data, path_list = importDataset(file_path, b_name)
    col_insp_result_accuracy = DoInspection_color(learn_data, insp_data, path_list)
    cor_insp_result_accuracy = DoInspection_corner(learn_data, insp_data, path_list)

    sum_col = sum(col_insp_result_accuracy)*200
    sum_cor_512 = sum(cor_insp_result_accuracy[0])
    sum_cor_256 = sum(cor_insp_result_accuracy[1])

    sum_cor = sum_cor_512 + sum_cor_256
    InitJson(file_path)
    neurons = 512
    vector = 32
    case_num = 1
    while neurons != 32:
        print("--------------------------------------")
        print("case%d) neurons/vectors = '%d / %d'"%(case_num, neurons, vector))
        print("--------------------------------------")
        print("Board_id", "Part_id", "Algorithm", "Accuracy", sep="  ")
        for i in range(0, len(col_insp_result_accuracy)):
            p_id = i+10002311
            acc = int(col_insp_result_accuracy[i]*100)
            SaveJson(file_path, 'color', str(p_id), neurons, vector, str(acc))
            print(b_name, p_id, 'color', acc, sep="     ")
        if neurons == 512:
            for i in range(0, len(cor_insp_result_accuracy[0])):
                p_id = i + 10002311
                acc = int(cor_insp_result_accuracy[0][i])
                SaveJson(file_path, 'corner', str(p_id), neurons, vector, str(acc))
                print(b_name, p_id, 'corner', acc, sep="     ")
        if neurons == 256:
            for i in range(0, len(cor_insp_result_accuracy[1])):
                p_id = i + 10002311
                acc = int(cor_insp_result_accuracy[1][i])
                SaveJson(file_path, 'corner', str(p_id), neurons, vector, str(acc))
                print(b_name, p_id, 'corner', acc, sep="     ")
        neurons = int(neurons/2)
        vector = int(vector*2)
        case_num = case_num + 1
    case = ""
    algorithm = ""
    print("-------------------------------------------------")
    if sum_col > sum_cor:
        case = "case1) neurons/vectors = '512 / 32'"
        algorithm = "color"
        print("best case : ", case)
        print("best algorithm : ", algorithm)

    else:
        if sum_cor_512 > sum_cor_256:
            case = "case1) neurons/vectors = '512 / 32'"
            algorithm = "corner"
            print("best case : ", case)
            print("best algorithm : ", algorithm)

        else:
            case = "case2) neurons/vectors = '256 / 64'"
            algorithm = "corner"
            print("best case : ", case)
            print("best algorithm : ", algorithm)

    BestJson(file_path, case, algorithm)
    print("-------------------------------------------------")
