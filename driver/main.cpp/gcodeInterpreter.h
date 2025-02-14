// gcodeInterpreter.cpp
#ifndef GCODE_INTER_H
#define GCODE_INTER_H
#include "stepperMotorDriver.h"

class GCodeInterpreter {
    public:
    GCodeInterpreter(MotorDriver& motorX, MotorDriver& motorY) : xMotor(motorX), yMotor(motorY) {}
    
    void parseCommand(String command);
    
    private:
    MotorDriver& xMotor;
    MotorDriver& yMotor;
};

#endif