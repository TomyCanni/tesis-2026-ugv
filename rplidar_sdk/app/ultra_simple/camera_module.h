#ifndef CAMERA_MODULE_H
#define CAMERA_MODULE_H

#include <opencv2/opencv.hpp>

// Inicializa la cámara USB
bool inicializarCamara(cv::VideoCapture& cap, int deviceID = 0, int width = 640, int height = 480);

// Captura un frame y lo devuelve
cv::Mat capturarCamara(cv::VideoCapture& cap);

#endif // CAMERA_MODULE_H