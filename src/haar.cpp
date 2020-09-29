#include "opencv2/objdetect.hpp"
#include "opencv2/videoio.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"

#include <stdio.h>
 
using namespace std;
using namespace cv;
 
void detect_face(){
    Mat src = imread("../data/face_y.jpg");

    if(src.empty()){
        printf("Image load failed!\n");
        return;
    }
    
    CascadeClassifier classifier("./haarcascade_frontalface_default.xml");

    if(classifier.empty()){
        printf("XML load failed!\n");
        return;
    }

    vector<Rect> faces;
    classifier.detectMultiScale(src, faces);

    for(Rect rc : faces){
        rectangle(src, rc, Scalar(255, 0, 255), 2);
    }
    if(faces.size() == 0){
        printf("0314228071\n");
    }
    else
    {
        printf("0314208071\n");
    }
    
    // imshow("src", src);
    // waitKey();
    // destroyAllWindows();
}

int main(){
    detect_face();
}