import numpy as np
import cv2
import matplotlib
import matplotlib.pyplot as plt
import calcMissing as hist

class inspection:
    def __init__(self):
        self.result_inspection = True

    def component_learn(self, x1, x2, y1, y2, b_name, p_name):
        img = cv2.imread('test.png')
        img=img[x1:x2, y1:y2] # crop
        cv2.imwrite('../' + b_name +' /' + p_name +'.jpg', img)

    def component_inspect(self, x1, x2, y1, y2, b_name, p_name):
        img_good = cv2.imread('../' + b_name +' /' + p_name + '.jpg') #learn data image
        img = cv2.imread('test.png') # classification data image
        img2=img.copy()
        img2=img2[x1:x2, y1:y2] # crop

        # corr값 확인
        start=cv2.getTickCount()
        corr=hist.HistCompareMissing(img_good, img2)            
        end=cv2.getTickCount()
        time=(end-start)/cv2.getTickFrequency()
        print('inspection time : ', time)
        
        if corr > 0.6 :
            print('U11 correlation value : ', corr)        
            self.result_inspection = True
        else :
            print('U11 error')
            self.result_inspection = False      

        return self.result_inspection

    def part_wrong(self, x1, x2, y1, y2, b_name, p_name):
        self.component_inspect(self, x1, x2, y1, y2, b_name, p_name)

    def parts_none(self, x1, x2, y1, y2, b_name, p_name):
        self.component_inspect(self, x1, x2, y1, y2, b_name, p_name)
