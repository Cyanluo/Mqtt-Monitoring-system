#include "Serial.h"

Serial::Serial()
{

}

Serial* Serial::NewSerial(const char *device, const int baud)
{
    Serial* ret = new Serial();

    if(ret != nullptr)
    {
        ret->m_fd = ret->serialOpen(device, baud);

        if(ret->m_fd == -1)
        {
            delete ret;
            ret = nullptr;
        }
    }

    return ret;
}

int Serial::serialOpen (const char *device, const int baud)
{
    return ::serialOpen(device, baud);
}

int Serial::serialDataAvail ()
{
    return ::serialDataAvail(m_fd);
}

int Serial::serialGetchar ()
{
    return ::serialGetchar(m_fd);
}

Serial::~Serial()
{
    ::serialClose(m_fd);
}
