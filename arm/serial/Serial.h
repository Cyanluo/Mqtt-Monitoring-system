#ifndef SERIAL_H
#define SERIAL_H

#include "AbstractSerial.h"
#include "wiringSerial.h"

class Serial: public AbstractSerial
{
protected:
    int m_fd;

    Serial();
    virtual int serialOpen (const char *device, const int baud);
public:
    static Serial* NewSerial(const char *device, const int baud);

    int serialDataAvail ();
    int serialGetchar ();
    ~Serial();
};

#endif // SERIAL_H
