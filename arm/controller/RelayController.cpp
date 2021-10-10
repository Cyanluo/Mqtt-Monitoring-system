#include "RelayController.h"
#include <iostream>

RelayController::RelayController(int pin): m_isControlComVaild(true), m_relay_time(1000)
{
    m_pinController = new PinController(pin);

    m_pinController->pinMode(OUTPUT);
    m_pinController->digitalWrite(0);

    m_relay_timer = new QTimer(this);
    m_relay_timer->setInterval(m_relay_time);

    connect(m_relay_timer, &QTimer::timeout, this, &RelayController::on_timeout);
}

void RelayController::on_timeout()
{
    m_isControlComVaild = true;

    m_relay_timer->stop();
}

void RelayController::set_relay_time(int microscoends)
{
    m_relay_time = microscoends;

    m_relay_timer->setInterval(m_relay_time);
}

bool RelayController::open()
{
    bool ret = false;

    if(m_isControlComVaild)
    {
        m_isControlComVaild = false;

        m_pinController->digitalWrite(1);

        std::cout << "open" << std::endl;

        m_relay_timer->start(m_relay_time);

        ret = true;
    }

    return ret;
}

bool RelayController::close()
{
    bool ret = false;

    if(m_isControlComVaild)
    {
        m_isControlComVaild = false;

        m_pinController->digitalWrite(0);

        std::cout << "close" << std::endl;

        m_relay_timer->start(m_relay_time);

        ret = true;
    }

    return ret;
}

RelayController::~RelayController()
{
    delete m_pinController;
}
