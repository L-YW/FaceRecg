#include "opencv2/objdetect.hpp"
#include "opencv2/videoio.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"

#include <wiringSerial.h>
#include <wiringPi.h>

#include <string.h>
#include <stdio.h>

#define BAUD    115200
using namespace std;
using namespace cv;

char serc[15] = "0314228071";

char detect_face(){
    int ser;
    
    Mat src = imread("../data/face_y.jpg");
    if(src.empty()){
        printf("Image load failed!\n");
        return 1;
    }
    
    CascadeClassifier classifier("./haarcascade_frontalface_default.xml");

    if(classifier.empty()){
        printf("XML load failed!\n");
        return 1;
    }

    vector<Rect> faces;
    classifier.detectMultiScale(src, faces);

    for(Rect rc : faces){
        rectangle(src, rc, Scalar(255, 0, 255), 2);
    }
    
    if(faces.size() == 0){
        serc[5] = '2';
    }
    else
    {
        serc[5] = '0';
    }
}
int main(){
    int fd;
    detect_face();
//    serc[5] = (char)(detect_face()+48);
    if((fd=serialOpen("/dev/ttyAMA0", BAUD)) < 0){
        printf("Device file open error!! use sudo ...\n");
        return 1;
    }    
    serialPuts(fd, serc);
    serialPutchar(fd, '\r');
    serialPutchar(fd, '\n');

    return 0;
}