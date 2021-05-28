import numpy as np
import cv2

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

    return dst

def __HistCalcMissingMulti(img, channel_num, bin_size = 256, showPlt=False) :
    histColor = ('b', 'g', 'r')
    for i in range(channel_num):
        hist = cv2.calcHist(images=[img], channels=[i], mask=None,
                        histSize=[bin_size], ranges=[0, 256])
    return hist

def __HistCalcMissing(img, bin_size = 256, showPlt=False) :
    hist = cv2.calcHist(images=[img], channels=[0], mask=None,
                        histSize=[bin_size], ranges=[0, 256])
    return hist

def __HistCompare(h1, h2, method = cv2.HISTCMP_CORREL) :
    e1 = cv2.getTickCount()
    cor = cv2.compareHist(h1, h2, method)
    e2 = cv2.getTickCount()
    time = (e2 - e1)/ cv2.getTickFrequency()
    #print("HistCompare Delay : ", time)
    return cor

def __HistCompare_YC(image1, image2, method = cv2.HISTCMP_CORREL, showPlt=False) :

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
    imgs.append(img1)
    imgs.append(img2)
    for img in imgs :
        if kmean > 0 :
            img = __KMeansMissing(img, kmean, showPlt)
        # img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hist_img = __HistCalcMissing(img, 256, showPlt)
        hists.append(cv2.normalize(hist_img, hist_img, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX))

    return __HistCompare(hists[0], hists[1])

def HistCompareMissing_Equalized (img1, img2, kmean=0, showPlt=False) :
    """
    img1과 img2의 히스토그램을 계산하고 비교합니다.
    평활화를 진행하고 계산합니다.
    """
    hsv_img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2HSV)
    hsv_img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)

    img1_h,img1_s,img1_v = cv2.split(hsv_img1)
    img2_h,img2_s,img2_v = cv2.split(hsv_img2)

    img1_equalizedV = cv2.equalizeHist(img1_v)
    img2_equalizedV = cv2.equalizeHist(img2_v)

    hsv_img1_eq = cv2.merge([img1_h,img1_s,img1_equalizedV])
    hsv_img2_eq = cv2.merge([img2_h,img2_s,img2_equalizedV])

    img1_eq = cv2.cvtColor(hsv_img1_eq,cv2.COLOR_HSV2BGR)
    img2_eq = cv2.cvtColor(hsv_img2_eq,cv2.COLOR_HSV2BGR)

    imgs = list()
    hists = list()
    imgs.append(img1_eq)
    imgs.append(img2_eq)
    for img in imgs :
        if kmean > 0 :
            img = __KMeansMissing(img, kmean, showPlt)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hist_img = __HistCalcMissing(img_hsv, 256, showPlt)
        hists.append(cv2.normalize(hist_img, hist_img, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX))

    return __HistCompare(hists[0], hists[1])

def __TestFunction() :
    img_ic_good = cv2.imread('../data/alpha_good_U11.jpg')
    img_ic_bad = cv2.imread('../data/alpha_bad_U11.jpg')
    print(HistCompareMissing(img_ic_good, img_ic_bad, 0, False))
def BinaryCheck(image1, image2, channel = 0, threshold = 100) :
    # channel =  0 : grayscale, 1 : red, 2 : green, 3 : blue
    image1_target = image1; image2_target = image2
    if channel == 0 :
        image1_target = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
        image1_target = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)
    else :
        b1, g1, r1 = cv2.split(image1_target)
        b2, g2, r2 = cv2.split(image2_target)
        if channel == 1:
            image1_target = r1
            image2_target = r2
        elif channel == 2:
            image1_target = g1
            image2_target = g2
        elif channel == 3:
            image1_target = b1
            image2_target = b2

    ret, binary1 = cv2.threshold(image1_target, threshold, 255, cv2.THRESH_BINARY)
    ret, binary2 = cv2.threshold(image2_target, threshold, 255, cv2.THRESH_BINARY)

    count1 = 0; count2 = 0

    for sero in range(binary1.shape[0]) :
        for garo in range(binary1.shape[1]):
            if binary1[sero,garo] == 0 :
                count1 += 1

    for sero in range(binary2.shape[0]) :
        for garo in range(binary2.shape[1]):
            if binary2[sero,garo] == 0 :
                count2 += 1

    if count1 == 0 and count2 == 0 :
        return 1.0

    bigger = count1 if count1 >= count2 else count2
    smaller = count2 if count2 < count1 else count1
    corr = smaller / bigger
    return corr