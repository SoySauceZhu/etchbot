#ifndef MOTOR_DRIVER_H
#define MOTOR_DRIVER_H
#include <Arduino.h>

class MotorDriver {
    public:
    MotorDriver(){};
    ~MotorDriver(){};

    void configure(short en, short step, short dir);

    void forward(unsigned long pulse, unsigned int feedrate) ;

    void backward(unsigned long pulse, unsigned int feedrate) ;

    void sendPulse(unsigned long pulse, unsigned int delay) ;
    
    void toOrigin();

    void toPosition(float pos, unsigned int feedrate) ;

    void setCoordinate(float pos) ;

    void invertDirection();
    

    private:
    short EN_PIN;
    short STEP_PIN;
    short DIR_PIN;
    unsigned long ABS_POS_PULSE;
    unsigned long OFFSET_POS_PULSE;
    unsigned int STEP_PER_MM = 6;
    bool REVERT_CALIBRATE = 0;
};

#endif  