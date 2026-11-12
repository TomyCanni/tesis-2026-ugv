#include "camera_module.h"
#include <iostream>

bool inicializarCamara(cv::VideoCapture& cap, int deviceID, int width, int height) {
    cap.open(deviceID);
    if (!cap.isOpened()) {
        std::cerr << "No se pudo abrir la cámara en el dispositivo " << deviceID << std::endl;
        return false;
    }
    cap.set(cv::CAP_PROP_FRAME_WIDTH, width);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, height);
    return true;
}

cv::Mat capturarCamara(cv::VideoCapture& cap) {
    cv::Mat frame;
    cap >> frame;
    return frame;
}