#include "stepperMotorDriver.h"

void MotorDriver::configure(short en, short step, short dir) {
    EN_PIN = en;
    STEP_PIN = step;
    DIR_PIN = dir;
    pinMode(EN_PIN, INPUT);
    pinMode(STEP_PIN, OUTPUT);
    pinMode(DIR_PIN, OUTPUT);
};

void MotorDriver::forward(unsigned long pulse, unsigned int feedrate) {
    digitalWrite(DIR_PIN, HIGH^REVERT_CALIBRATE);
    unsigned int delay = (unsigned int) 60000000 / (feedrate * STEP_PER_MM);
    sendPulse(pulse, delay);
    ABS_POS_PULSE += pulse;   
};

void MotorDriver::backward(unsigned long pulse, unsigned int feedrate) {
    digitalWrite(DIR_PIN, LOW^REVERT_CALIBRATE);
    unsigned int delay = (unsigned int) 60000000 / (feedrate * STEP_PER_MM);
    sendPulse(pulse, delay);
    ABS_POS_PULSE -= pulse;
};

void MotorDriver::sendPulse(unsigned long pulse, unsigned int delay) {
    for(unsigned long i = 0; i < pulse; i++) {
        digitalWrite(STEP_PIN, HIGH);
        delayMicroseconds(delay);
        digitalWrite(STEP_PIN, LOW);
        delayMicroseconds(delay);
    }
};

void MotorDriver::toOrigin(){
};

void MotorDriver::toPosition(float pos, unsigned int feedrate) {
    unsigned long targetPulse = pos * STEP_PER_MM;
    long dPulse = (long) targetPulse - ABS_POS_PULSE + OFFSET_POS_PULSE;
    if (dPulse > 0) forward(dPulse, feedrate);
    else if (dPulse < 0) backward(dPulse, feedrate);        // TODO
};

void MotorDriver::setCoordinate(float pos) {
    OFFSET_POS_PULSE = ABS_POS_PULSE - pos * STEP_PER_MM;
};

void MotorDriver::invertDirection(){
    REVERT_CALIBRATE = !REVERT_CALIBRATE;
};

