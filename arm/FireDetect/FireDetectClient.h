#ifndef WIDGET_H
#define WIDGET_H

#include <QObject>

#include "../networkHandle/MqttHandle.h"
#include "../Pointer/SharedPointer.h"
#include "../Pointer/SmartPointer.h"
#include "../sensor/GYSerialTempSensor.h"
#include "../serial/Serial.h"
#include "../controller/RelayController.h"

#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;

class FireDetectClient : public QObject
{
    Q_OBJECT

    SharedPointer<AbstractSerial> m_serial;
    SmartPointer<GYSerialTempSensor> m_tempSensor;
    SmartPointer<MqttHandle> m_mqttClient;
    SmartPointer<RelayController> m_relayController;
    VideoCapture m_capture;

public:
    FireDetectClient(QObject *parent = 0);

//slots
    void on_recv_control_signal(QString c_msg);
    void send_img();
    ~FireDetectClient();
};

#endif // WIDGET_H
