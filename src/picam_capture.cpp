#include <iostream>
#include <raspicam/raspicam_cv.h>
#include <opencv2/imgproc.hpp>

#include "opencv2/objdetect.hpp"
#include "opencv2/videoio.hpp"
#include "opencv2/highgui.hpp"

#include <wiringSerial.h>
#include <wiringPi.h>

#include <string.h>
#include <stdio.h>
using namespace std;
using namespace cv;
 
#define BAUD    115200


int main(){
    char serc[15] = "0314228071";
    raspicam::RaspiCam_Cv Camera;
    Mat image;
 
    Camera.set( CV_CAP_PROP_FORMAT, CV_8UC3);
    Camera.set( CV_CAP_PROP_FRAME_WIDTH, 320 ); //320*240
    Camera.set( CV_CAP_PROP_FRAME_HEIGHT, 240 );
 
 
    if (!Camera.open()) {cerr<<"Error opening the camera"<<endl;return -1;}
    int fd;
    if((fd=serialOpen("/dev/ttyAMA0", BAUD)) < 0){
        printf("Device file open error!! use sudo ...\n");
        return 1;
    } 
    while(1){

        Camera.grab();
        Camera.retrieve (image);
 
        //cvtColor(image, image, cv::COLOR_BGR2RGB);
 
        // imshow( "picamera test", image );
        
        
        Mat src = Camera.read(image);
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
        classifier.detectMultiScale(src, faces); // +0.1

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
        printf("%s\n", serc);
        // serialPuts(fd, serc);
        // serialPutchar(fd, '\r');
        // serialPutchar(fd, '\n');
        if ( waitKey(20) == 27 ) break; //ESC키 누르면 종료
    }

    Camera.release();

    return 0;
}
