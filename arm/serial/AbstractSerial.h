#ifndef ABSTRACTSERIAL_H
#define ABSTRACTSERIAL_H

class AbstractSerial
{
protected:
    AbstractSerial(const AbstractSerial&);
    AbstractSerial& operator = (const AbstractSerial&);
public:
    AbstractSerial(){}
    virtual int serialDataAvail () = 0;
    virtual int serialGetchar () = 0;
    virtual ~AbstractSerial(){}
};


#endif // ABSTRACTSERIAL_H
