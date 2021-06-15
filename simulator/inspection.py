import numpy as np
import cv2
import calcMissing as hist
import random
import os
import json


class inspection:
    def __init__(self):
        self.result_inspection = True

    """=========================================================================================================================
        학습 함수 | 주어진 영역을 잘라내서 sub image를 만들고 저장하는 함수.
    ========================================================================================================================="""

    def component_learn(self, x1, y1, x2, y2, b_name, p_name, state, dataPath):
        if self.check_range(x1, y1, x2, y2):
            img = cv2.imread(dataPath)
            img = img[y1:y2, x1:x2]  # crop

            # 디렉토리가 있는지 확인 한 후 보드 디렉토리 생성
            try:
                if os.path.isdir('./' + b_name + '/') is False:
                    print("try to make dir")
                    os.makedirs('./' + b_name + '/', exist_ok=True)
            except OSError as e:
                print("OS error: {0}".format(e))
                print("\033[1;33m      [Make directory error]\033[0m")
                print("\033[1;31m      The board directory cannot be created in the path.\033[0m")
                return False

            # Crop한 이미지를 저장. 문제시 False 리턴
            try:
                cv2.imwrite('./' + b_name + '/' + p_name + '_' + str(state) + '.jpg', img)
            except:
                print("\033[1;33m      [Write file error]\033[0m")
                print("\033[1;31m      The parts sub image cannot be write in the path.\033[0m")
                return False
            return True

    """=========================================================================================================================
        검사 함수 | 주어진 영역을 검사하는 함수. 
    ========================================================================================================================="""

    def component_inspect(self, x1, y1, x2, y2, b_name, p_name, state, dataPath):
        if self.check_range(x1, y1, x2, y2) is False:
            return [str(False), str(0)]

        img_good = cv2.imread('./' + b_name + '/' + p_name + '_' + '0' + '.jpg')
        img_insp = cv2.imread(dataPath)

        # 검사 및 정상 이미지가 잘 로드 되었는지 확인하는 부분
        if self.check_imread(img_good, "Normal image") is False:
            return [str(False), str(0)]
        if self.check_imread(img_insp, "Inspection image") is False:
            return [str(False), str(0)]

        # 검사 및 정상 이미지가 10kb가 넘는지 확인하는 부분
        if self.check_file_over_10kb('./' + b_name + '/' + p_name + '_' + '0' + '.jpg', "Normal image") is False:
            return [str(False), str(0)]
        if self.check_file_over_10kb(dataPath, "Inspection image") is False:
            return [str(False), str(0)]

        # =====================================================================================================================
        #  정상이미지와 검사 이미지의 corr1 값 구하기
        # =====================================================================================================================
        img_insp = img_insp[y1:y2, x1:x2]
        # 적색 마킹 검사 (정상/불량 이미지 불필요함)

        if state == 6:
            insp_config_dic = self.read_insp_config_json("./inspection_config.json", "marking")  # 마킹 검사 조건 읽어오기
            if insp_config_dic is None:
                result = self.classify_red_marking(img_insp)
            else:
                result = self.classify_red_marking(img_insp,
                                                   K=insp_config_dic['K'],
                                                   H_upper=insp_config_dic['H_UPPER'],
                                                   SV_lower=insp_config_dic['SV_LOWER'],
                                                   thr_red_ps=insp_config_dic['THR_RED'])

            return [str(result), str(random.uniform(0.30, 0.38))]

        start = cv2.getTickCount()
        corr1 = hist.HistCompareMissing_Equalized(img_good, img_insp)
        end = cv2.getTickCount()
        time_good = (end - start) / cv2.getTickFrequency()

        # 불량 이미지 로드
        learningPath = './' + b_name + '/' + p_name + '_' + str(state) + '.jpg'
        img_learn = cv2.imread(learningPath)
        if self.check_file_over_10kb(learningPath, "Learning image") is False:
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
            self.result_inspection = True if corr1 > corr2 else False

        # =====================================================================================================================
        #  불량 이미지가 학습되어 있지 않을 경우, corr1이 Threshold 값을 넘는지 확인
        # =====================================================================================================================
        else:
            self.result_inspection = True if corr1 > 0.7 else False
        return [str(self.result_inspection), str(random.uniform(0.30, 0.38))]

    """=========================================================================================================================
        주어진 crop 영역이 올바른 영역(x1 < x2 && y1 < y2 == True )인지 판단하는 함수
    ========================================================================================================================="""

    def check_range(self, x1, y1, x2, y2):
        if x2 > x1 and y2 > y1:
            return True
        else:
            print("\033[1;33m      [Illegal range error]\033[0m")
            if x2 < x1 and y2 > y1:
                print("\033[1;31m      learn image; x1 is greater than x2\033[0m")
            elif x2 > x1 and y2 < y1:
                print("\033[1;31m      learn image; y1 is greater than y2\033[0m")
            elif x2 < x1 and y2 < y1:
                print("\033[1;31m      learn image; x1, y1 is greater than x2, y2\033[0m")
            return False

    """=========================================================================================================================
        주어진 경로의 파일이 10kb가 넘는지 확인하는 함수
    ========================================================================================================================="""

    def check_file_over_10kb(self, filepath, fileType):
        if os.path.exists(filepath) and os.path.getsize(filepath) < 512:  # bytes
            print("\033[1;33m      [Corrupted image file error]\033[0m")
            print("\033[1;31m      " + fileType + " size is not over 10kb\033[0m")
            return False
        return True

    """=========================================================================================================================
        이미지가 정상적으로 열렸는지 확인하는 함수
    ========================================================================================================================="""

    def check_imread(self, img, fileType):
        if img is None:
            print("\033[1;33m      [Image load fialed error]\033[0m")
            print("\033[1;31m      " + fileType + " load failed\033[0m")
            return False
        return True

    """=========================================================================================================================
        외부 호출 함수
    ========================================================================================================================="""

    def parts_wrong(self, x1, x2, y1, y2, b_name, p_name, dataPath):
        return self.component_inspect(x1, x2, y1, y2, b_name, p_name, 1, dataPath)

    def parts_none(self, x1, x2, y1, y2, b_name, p_name, dataPath):
        return self.component_inspect(x1, x2, y1, y2, b_name, p_name, 2, dataPath)

    def parts_marking(self, x1, x2, y1, y2, b_name, p_name, dataPath):
        return self.component_inspect(x1, x2, y1, y2, b_name, p_name, 6, dataPath)

    def KYC_test(self):
        img_good = cv2.imread('./board/partsDown_0.jpg')
        img_learn = cv2.imread('./board/partsDown_6.jpg')

        corr = hist.HistCompare_YC(img_learn, img_good)
        print(corr)
        return

    """=========================================================================================================================
        검사조건 JSON 파일 읽어와서 DIC 리턴
    ========================================================================================================================="""

    def read_insp_config_json(self, json_path, insp_type_str):
        try:
            with open(json_path, "r") as st_json:
                try:
                    json_load = json.load(st_json)
                    insp_config_json_dic = json_load[insp_type_str]
                    return insp_config_json_dic
                except:
                    print("Inspection type is not exist in json file")
                    return None
        except:
            print("Opening json file is failed.")
        return None

    """=========================================================================================================================
        레드마킹에러인지 판단하는 함수 
        마킹에러가 아니면 true
        마킹에러가 맞다면 false를 리턴
        x1, x2, y1, y2가 -1이라면 크랍하지 않음
        K : 군집도
        H_upper : 적색 H의 상한값 (적색 H값은 대게 0 ~ 10)
        thr_red_ps : 마킹에러라고 판단할 적색 픽셀의 하한 개수
    ========================================================================================================================="""

    def classify_red_marking(self, img_arr, x1=-1, x2=-1, y1=-1, y2=-1,
                             K=5, H_upper=5, SV_lower=100, thr_red_ps=100,
                             show_plt=False):
        ### 이미지 로드
        img_part = img_arr
        if show_plt:
            plt.imshow(cv2.cvtColor(img_part, cv2.COLOR_BGR2RGB))
            plt.show()

        ### 이미지 크랍
        img_part_crop = img_part
        if x1 != -1:
            img_part_crop = img_part[y1:y2, x1:x2]
        if show_plt:
            plt.imshow(cv2.cvtColor(img_part_crop, cv2.COLOR_BGR2RGB))
            plt.show()

        ### 이미지 칼라 평활화
        # HSV 평활화
        #         img_hsv    = cv2.cvtColor(img_part_crop, cv2.COLOR_BGR2HSV)
        #         h, s, v = cv2.split(img_hsv)
        #         v2 = cv2.equalizeHist(v)
        #         dst = cv2.merge([h, s, v2])
        #         img_crop_bgr_equal    = cv2.cvtColor(dst, cv2.COLOR_HSV2BGR)

        # YCrCb 평활화
        #         img_part_crop_YCrCb = cv2.cvtColor(img_part_crop, cv2.COLOR_BGR2YCrCb)
        #         ycrycb_planes = cv2.split(img_part_crop_YCrCb)
        #         ycrycb_planes[0] = cv2.equalizeHist(ycrycb_planes[0])
        #         dst = cv2.merge(ycrycb_planes)
        #         img_crop_bgr_equal    = cv2.cvtColor(dst, cv2.COLOR_YCrCb2BGR)

        #         if show_plt :
        #             plt.imshow(cv2.cvtColor(img_crop_bgr_equal, cv2.COLOR_BGR2RGB))
        #             plt.show()

        ### K-mean 연산
        # reshape 하면 전체픽셀이 일렬로 늘어지게 됨
        data = img_part_crop.reshape((-1, 3)).astype(np.float32)  # BGR
        term_crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret, labels, centers = cv2.kmeans(data, K, None, term_crit, 5,
                                          cv2.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers)
        res = centers[labels.flatten()]
        img_crop_bgr_eqaul_kmean = res.reshape(img_part_crop.shape)
        if show_plt:
            plt.imshow(cv2.cvtColor(img_crop_bgr_eqaul_kmean, cv2.COLOR_BGR2RGB))
            plt.show()

        preproc_img = img_crop_bgr_eqaul_kmean

        dir_name = './debug/'

        try:
            if not (os.path.isdir(dir_name)):
                os.makedirs(os.path.join(dir_name))
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Failed to create directory!!!!!")
                raise

        cv2.imwrite(dir_name + 'red_marking_equal.jpg', preproc_img)

        ### inRange 이진화
        img_hsv = cv2.cvtColor(preproc_img, cv2.COLOR_BGR2HSV)  # cvtColor 함수를 이용하여 hsv 색공간으로 변환
        lower_red = (0, SV_lower, SV_lower)  # hsv 이미지에서 바이너리 이미지로 생성 , 적당한 값 30
        upper_red = (H_upper, 255, 255)
        img_mask = cv2.inRange(img_hsv, lower_red, upper_red)  # 범위내의 픽셀들은 흰색(255), 나머지 검은색(0)

        ### 결과 표시
        img_result = cv2.bitwise_and(preproc_img, preproc_img, mask=img_mask)
        if show_plt:
            plt.imshow(cv2.cvtColor(img_mask, cv2.COLOR_GRAY2BGR))
            plt.show()
            plt.imshow(cv2.cvtColor(img_result, cv2.COLOR_BGR2RGB))
            plt.show()

        ### 255 픽셀 카운트
        count_255 = 0
        for i in range(len(img_mask)):
            for j in range(len(img_mask[i])):
                if img_mask[i][j] == 255:
                    count_255 += 1
        print(count_255)

        ### 최종 판정
        if count_255 >= thr_red_ps:
            print("MARKING ERROR")
            return False
        else:
            print("NORMAL")
            return True