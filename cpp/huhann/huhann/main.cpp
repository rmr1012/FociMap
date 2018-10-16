//
//  main.cpp
//  huhann
//
//  Created by Dennis Ren on 10/16/18.
//  Copyright © 2018 Dennis Ren. All rights reserved.
//

#include <iostream>

#include <chrono>
#include <opencv2/opencv.hpp>
cv::Mat huHann(cv::Mat img);


int main(int argc, const char * argv[]) {
    // insert code here...
    std::cout << "Hello, World!\n";
    cv::Mat img;
    img= cv::imread("/Users/dennisren/Downloads/IMGP2396.JPG",CV_LOAD_IMAGE_GRAYSCALE );
    cv::Mat result;
    auto start = std::chrono::high_resolution_clock::now();
    result = huHann(img);
    auto stop =  std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);
    
    // To get the value of duration use the count()
    // member function on the duration object
    std::cout << duration.count() << std::endl;
//std::cout<<result;
    cv::imwrite("/Users/dennisren/alpha.png", result*255);
    return 0;
}


//def huHann(img): # input 2d image
cv::Mat huHann(cv::Mat img){
//
//#print("step 0")
//
//#print("step 1")
    int sigmaA=7;
    int sigmaB=9;
//sigmaA=8
//sigmaB=10
//#print("step 2")
//sigmaMax=max(sigmaA,sigmaB)
    int sigmaMax=std::max(sigmaA,sigmaB);

//fsz=[sigmaMax, sigmaMax] # function size
//#print("step 3")
//kernelA=matlab_style_gauss2D(fsz,sigmaA)
//kernelB=matlab_style_gauss2D(fsz,sigmaB)
//#print("step 4")
    cv::Mat imgA;
    cv::GaussianBlur( img, imgA, cv::Size(sigmaMax,sigmaMax), sigmaA, sigmaA );
    cv::Mat imgB;
    cv::GaussianBlur( img, imgB, cv::Size(sigmaMax,sigmaMax), sigmaB, sigmaB );
//#print("step 5")
    cv::Mat R1=img-imgA;
    cv::Mat R2=imgA-imgB;
//#print("step 6")
//#print("step 7")
//R=np.divide(R1,R2)
    cv::Mat R;
    cv::divide(R1,R2,R);
//R[R == -inf] = 0
//R[R == inf] = 0
//R=np.nan_to_num(R)
//#print("step 8")
//Rf=scipy.ndimage.maximum_filter(R,size=8)
    cv::Mat kernel;
    kernel = cv::getStructuringElement( cv::MORPH_RECT,cv::Size(8,8));
    cv::Mat Rf;
    // Perform max filtering on image using dilate
    cv::dilate(R, Rf, kernel);
//#print("step 9")
//blurmap=np.divide((np.multiply(sigmaA,sigmaB)),(np.multiply((sigmaB-sigmaA),Rf)+sigmaB))
    cv::Mat blurmap;
    cv::divide(sigmaA*sigmaB,(sigmaB-sigmaA)*Rf+sigmaB,blurmap);
//#print("step 10")
    blurmap= 1/(8-blurmap);
    
    return blurmap;
    
}
