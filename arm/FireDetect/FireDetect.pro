#-------------------------------------------------
#
# Project created by QtCreator 2021-04-30T21:36:46
#
#-------------------------------------------------

QT       += core gui
QT += network

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = FireDetect
TEMPLATE = app

# The following define makes your compiler emit warnings if you use
# any feature of Qt which has been marked as deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if you use deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

LIBS += /usr/local/lib/libopencv_* -lwiringPi -lcrypt -lpthread -lm -lrt

SOURCES += \
    ../Pointer/Exception.cpp \
    ../Pointer/Object.cpp \
    ../networkHandle/MqttHandle.cpp \
    ../qmqtt/qmqtt_client.cpp \
    ../qmqtt/qmqtt_client_p.cpp \
    ../qmqtt/qmqtt_frame.cpp \
    ../qmqtt/qmqtt_message.cpp \
    ../qmqtt/qmqtt_network.cpp \
    ../qmqtt/qmqtt_router.cpp \
    ../qmqtt/qmqtt_routesubscription.cpp \
    ../qmqtt/qmqtt_socket.cpp \
    ../qmqtt/qmqtt_ssl_socket.cpp \
    ../qmqtt/qmqtt_timer.cpp \
    ../qmqtt/qmqtt_websocket.cpp \
    ../qmqtt/qmqtt_websocketiodevice.cpp \
    ../sensor/GYSerialTempSensor.cpp \
    ../serial/Serial.cpp \
    FireDetectClient.cpp \
        main.cpp \
    ../serial/wiringSerial.c \
    ../controller/PinController.cpp \
    ../controller/RelayController.cpp

HEADERS += \
    ../Pointer/Exception.h \
    ../Pointer/Object.h \
    ../Pointer/Pointer.h \
    ../Pointer/SharedPointer.h \
    ../Pointer/SmartPointer.h \
    ../networkHandle/MqttHandle.h \
    ../qmqtt/qmqtt.h \
    ../qmqtt/qmqtt_client.h \
    ../qmqtt/qmqtt_client_p.h \
    ../qmqtt/qmqtt_frame.h \
    ../qmqtt/qmqtt_global.h \
    ../qmqtt/qmqtt_message.h \
    ../qmqtt/qmqtt_message_p.h \
    ../qmqtt/qmqtt_network_p.h \
    ../qmqtt/qmqtt_networkinterface.h \
    ../qmqtt/qmqtt_routedmessage.h \
    ../qmqtt/qmqtt_router.h \
    ../qmqtt/qmqtt_routesubscription.h \
    ../qmqtt/qmqtt_socket_p.h \
    ../qmqtt/qmqtt_socketinterface.h \
    ../qmqtt/qmqtt_ssl_socket_p.h \
    ../qmqtt/qmqtt_timer_p.h \
    ../qmqtt/qmqtt_timerinterface.h \
    ../qmqtt/qmqtt_websocket_p.h \
    ../qmqtt/qmqtt_websocketiodevice_p.h \
    ../sensor/GYSerialTempSensor.h \
    ../sensor/Sensor.h \
    ../sensor/TempSensor.h \
    ../serial/AbstractSerial.h \
    ../serial/Serial.h \
    ../serial/wiringSerial.h \
    FireDetectClient.h \
    ../controller/PinController.h \
    ../controller/RelayController.h


INCLUDEPATH += /usr/local/include \
                /usr/local/include/opencv2

LIBS += /usr/local/lib/libopencv_*
