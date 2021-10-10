#ifndef SMARTPOINTER_H
#define SMARTPOINTER_H

#include "Pointer.h"

namespace FD
{

template <typename T>
class SmartPointer: public Pointer<T>
{
public:
    SmartPointer(T* pointer = NULL) : Pointer<T>(pointer)
    {

    }

    SmartPointer(const SmartPointer<T>& obj) : Pointer<T>(NULL)
    {
        this->m_pointer = obj.m_pointer;

        const_cast<SmartPointer<T>&>(obj).m_pointer = NULL;
    }

    SmartPointer<T>& operator =(const SmartPointer<T>& obj)
    {
        if(this != &obj)
        {
            T* p = this->m_pointer;

            this->m_pointer = obj.m_pointer;

            const_cast<SmartPointer<T>&>(obj).m_pointer = NULL;

            delete p;
        }
    }

    ~SmartPointer()
    {
        delete this->m_pointer;
    }
};

}

#endif // SMARTPOINTER_H

