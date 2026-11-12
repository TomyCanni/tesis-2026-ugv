#ifndef LIDAR_UTILS_H
#define LIDAR_UTILS_H

#include <opencv2/opencv.hpp>
#include "sl_lidar.h"
#include "sl_lidar_driver.h"

using namespace sl;

// Envía el mapa LIDAR codificado en JPEG por socket
void enviarMapaLidar(ILidarDriver* drv, int cx, int cy, int sockfd);

#endif // LIDAR_UTILS_H