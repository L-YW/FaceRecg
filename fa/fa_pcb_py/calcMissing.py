import numpy as np
import cv2
import matplotlib
import matplotlib.pyplot as plt


def __KMeansMissing(img, K, showPlt=False) :
    src = img
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV) #HSV 칼라스페이스로 교체

    #reshape 하면 전체픽셀이 일렬로 늘어지게 됨
    data = src.reshape((-1,3)).astype(np.float32) #BGR
    #data = hsv.reshape((-1,3)).astype(np.float32) #HSV

    term_crit=(cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, labels, centers = cv2.kmeans(data, K, None, term_crit, 5,
                                      cv2.KMEANS_RANDOM_CENTERS)
    #print('centers.shape=', centers.shape)
    #print('labels.shape=', labels.shape)
    #print('ret=', ret)
    #print('centers=', centers)
    #print('H Val Mean = ', centers[:,0].mean())

    centers = np.uint8(centers)
    res   = centers[labels.flatten()]
    dst  = res.reshape(src.shape)
    if showPlt == True :
        plt.imshow(cv2.cvtColor(dst, cv2.COLOR_BGR2RGB))
        plt.show()
    
    return dst

def __HistCalcMissingMulti(img, channel_num, bin_size = 256, showPlt=False) :
    histColor = ('b', 'g', 'r')
    for i in range(channel_num):
        hist = cv2.calcHist(images=[img], channels=[i], mask=None,
                        histSize=[bin_size], ranges=[0, 256])
        if showPlt == True :
            plt.plot(hist, color = histColor[i])
    if showPlt == True :
        plt.show()
    return hist

def __HistCalcMissing(img, bin_size = 256, showPlt=False) :
    hist = cv2.calcHist(images=[img], channels=[0], mask=None,
                        histSize=[bin_size], ranges=[0, 256])
    if showPlt == True :
        plt.plot(hist, color = 'b')
        plt.show()
    
    return hist
        
def __HistCompare(h1, h2, method = cv2.HISTCMP_CORREL) :
    e1 = cv2.getTickCount()
    cor = cv2.compareHist(h1, h2, method)
    e2 = cv2.getTickCount()
    time = (e2 - e1)/ cv2.getTickFrequency()
    #print("HistCompare Delay : ", time)
    return cor

def __HistCompare_YC(image1, image2, method = cv2.HISTCMP_CORREL, showPlt=False) :
    if showPlt == True :
        plt.subplot(1,2,1)
        plt.imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
        plt.subplot(1,2,2)
        plt.imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
        plt.show()
            
    hist1 = __HistCalcMissingMulti(image1, 3, 256, showPlt)
    hist2 = __HistCalcMissingMulti(image2, 3, 256, showPlt)
    e1 = cv2.getTickCount()
    cor = cv2.compareHist(hist1, hist2, method)
    e2 = cv2.getTickCount()
    time = (e2 - e1)/ cv2.getTickFrequency()
    print("HistCompare Delay : ", time)
    print(cor)
    return cor
    
def HistCompareMissing (img1, img2, kmean=0, showPlt=False) :
    """
    img1과 img2의 히스토그램을 계산하고 비교합니다.
    :kmean : k-군집화에서의 k값을 의미하며 0 보다 크면 수행합니다.
    :showPlt : 중간 계산과정에서 이미지의 변형 과정을 plot 합니다
    :return: 두 이미지의 Correlation 값
    """    
    imgs = list()
    hists = list()
    imgs.append(img1.copy())
    imgs.append(img2.copy())
    for img in imgs :
        if showPlt == True :
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            plt.show()
        if kmean > 0 :
            img = __KMeansMissing(img, kmean, showPlt)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hist_img = __HistCalcMissing(img, 256, showPlt)
        hists.append(cv2.normalize(hist_img, hist_img, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX))
    
    return __HistCompare(hists[0], hists[1])

def __TestFunction() :
    img_ic_good = cv2.imread('../data/alpha_good_U11.jpg')
    img_ic_bad = cv2.imread('../data/alpha_bad_U11.jpg')
    print(HistCompareMissing(img_ic_good, img_ic_bad, 0, False))
    