#include "FireDetectClient.h"
#include <QTimer>
#include <QDebug>
#include <wiringPi.h>

FireDetectClient::FireDetectClient(QObject *parent)
    : QObject(parent)
{
    m_serial = Serial::NewSerial("/dev/ttyS4", 9600);

    m_tempSensor = new GYSerialTempSensor(m_serial);

    Login_config log_info =
    {
        QHostAddress("192.168.43.226"),
        "public",
        1883,
        "1234",
        "admin"
    };

    m_mqttClient = new MqttHandle(log_info);

    connect(m_mqttClient.get(), &MqttHandle::control_signal, this, &FireDetectClient::on_recv_control_signal);

    m_capture.open(10);

    m_relayController = new RelayController(8);
    m_relayController->set_relay_time(6000);

    QTimer *timer = new QTimer(this);
    connect(timer, &QTimer::timeout, this, &FireDetectClient::send_img);
    timer->start(500);
}

void FireDetectClient::on_recv_control_signal(QString c_msg)
{
    bool ok = false;

    if(c_msg == "open")
    {
        ok = m_relayController->open();
    }
    else if(c_msg == "close")
    {
        ok = m_relayController->close();
    }
}

void FireDetectClient::send_img()
{
    Mat img;

    m_capture >> img;

    m_mqttClient->Publich_img(img);

    ST_Tempture temp = m_tempSensor->getData();

    if(temp.to > 50)
    {
        m_relayController->open();
    }
    else
    {
        // m_relayController->close();
    }
}

FireDetectClient::~FireDetectClient()
{

}
