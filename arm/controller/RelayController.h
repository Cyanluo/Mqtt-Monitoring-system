#ifndef RELAYCONTROLLER_H
#define RELAYCONTROLLER_H

#include <QObject>
#include <QTimer>
#include "PinController.h"

class RelayController: public QObject
{
    Q_OBJECT

    bool m_isControlComVaild;

    PinController* m_pinController;
    QTimer* m_relay_timer;

    int m_relay_time;

    void on_timeout();
public:
    RelayController(int pin);
    void set_relay_time(int microscoends);
    bool open();
    bool close();

    ~RelayController();
};

#endif // RELAYCONTROLLER_H
