#include "opencv2/objdetect.hpp"
#include "opencv2/videoio.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"
 
#include <iostream>
#include <stdio.h>
 
using namespace std;
using namespace cv;
 
void detect_face(){
    Mat src = imread("../data/kids.png");

    if(src.empty()){
        cerr << "Image load failed!" << endl;
        return;
    }
    
    CascadeClassifier classifier("haarcacade_frontalface_default.xml");

    if(classifier.empty()){
        cerr << "XML load failed!" << endl;
        return;
    }

    vector<Rect> faces;
    classifier.detectMultiScale(src, faces);

    fr(Rect rc : faces){
        rectangle(src, rc, Scalar(255, 0, 255), 2);
    }
    imshow("src", src);
    waitKey();
    destroyAllWindows();
}