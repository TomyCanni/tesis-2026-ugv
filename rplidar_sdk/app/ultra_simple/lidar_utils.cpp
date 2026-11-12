#include "lidar_utils.h"
#include <arpa/inet.h>   // sockets Linux
#include <unistd.h>
#define _USE_MATH_DEFINES
#include <cmath>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

// Función que abre un socket y envía cada frame
void enviarMapaLidar(ILidarDriver* drv, int cx, int cy, int sockfd) {
    sl_lidar_response_measurement_node_hq_t nodes[8192];
    size_t count = sizeof(nodes) / sizeof(nodes[0]);

    sl_result op_result = drv->grabScanDataHq(nodes, count);
    cv::Mat img(800, 800, CV_8UC3, cv::Scalar(0,0,0));

    if (SL_IS_OK(op_result)) {
        drv->ascendScanData(nodes, count);

        for (int pos = 0; pos < (int)count; ++pos) {
            float angle = (nodes[pos].angle_z_q14 * 90.f) / 16384.f;
            float dist  = nodes[pos].dist_mm_q2 / 4.0f;

            if (dist > 0) {
                float x = dist * cos(angle * M_PI / 180.0f);
                float y = dist * sin(angle * M_PI / 180.0f);

                int px = cx + (int)(x / 10.0f);
                int py = cy - (int)(y / 10.0f);

                cv::circle(img, cv::Point(px, py), 1, cv::Scalar(0,255,0), -1);
            }
        }

        // Codificar en JPEG
        std::vector<uchar> buf;
        cv::imencode(".jpg", img, buf);

        // Enviar tamaño + datos
        uint32_t size = buf.size();
        send(sockfd, &size, sizeof(size), 0);
        send(sockfd, buf.data(), buf.size(), 0);
    }
}