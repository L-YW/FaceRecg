import cv2


"""=========================================================================================================================
    이미지가 정상적으로 열렸는지 확인하는 함수
========================================================================================================================="""

def check_imread(img, fileType):
    if img is None:
        print("\033[1;33m      [Image load fialed error]\033[0m")
        print("\033[1;31m      " + fileType + " load failed\033[0m")
        return False
    return True

def calcCorner(img_good, img_insp):

    sift = cv2.SIFT_create()
    keypoints_good, descriptors_good = sift.detectAndCompute(img_good, None)
    keypoints_insp, descriptors_insp = sift.detectAndCompute(img_insp, None)

    BFMatcher = cv2.BFMatcher()

    matches = BFMatcher.knnMatch(descriptors_insp, descriptors_good, k=2)

    accuracy = []
    good =[]
    if len(matches) > 512:
        for m, n in matches[:512]:
            if m.distance < 0.75*n.distance:
                good.append([m])
        accuracy.append(len(good)/512*100)
    if len(matches) <= 512:
        for m, n in matches:
            if m.distance < 0.75*n.distance:
                good.append([m])
        accuracy.append(len(good)/len(matches)*100)

    good = []
    if len(matches) > 256:
        for m, n in matches[:256]:
            if m.distance < 0.75*n.distance:
                good.append([m])
        accuracy.append(len(good)/256*100)
    if len(matches) <= 256:
        for m, n in matches:
            if m.distance < 0.75*n.distance:
                good.append([m])
        accuracy.append(len(good)/256*100)

    return accuracy