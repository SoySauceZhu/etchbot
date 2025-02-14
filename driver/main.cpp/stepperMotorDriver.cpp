// stepperMotorDriver.cpp
#include "stepperMotorDriver.h"

void MotorDriver::configure(short en, short step, short dir) {
    EN_PIN = en;
    STEP_PIN = step;
    DIR_PIN = dir;
    pinMode(EN_PIN, OUTPUT);
    pinMode(STEP_PIN, OUTPUT);
    pinMode(DIR_PIN, OUTPUT);
    digitalWrite(EN_PIN, LOW);
}

long MotorDriver::getCurrentPosition() {
    return ABS_POS_PULSE;
}

void MotorDriver::forward(unsigned long pulse, unsigned int feedrate) {
    digitalWrite(DIR_PIN, HIGH ^ REVERT_CALIBRATE);
    stepDelay = 60000000 / (feedrate * STEP_PER_MM);
    pulsesRemaining = pulse;
    isMoving = true;
}

void MotorDriver::backward(unsigned long pulse, unsigned int feedrate) {
    digitalWrite(DIR_PIN, LOW ^ REVERT_CALIBRATE);
    stepDelay = 60000000 / (feedrate * STEP_PER_MM);
    pulsesRemaining = pulse;
    isMoving = true;
}

void MotorDriver::stepNonBlocking() {
    if (isMoving && pulsesRemaining > 0) {
        unsigned long now = micros();
        if (now - lastStepTime >= stepDelay) {
            lastStepTime = now;
            digitalWrite(STEP_PIN, HIGH);
            delayMicroseconds(2);
            digitalWrite(STEP_PIN, LOW);
            pulsesRemaining--;
        }
        // update ABS_POS_PULSE
        ABS_POS_PULSE += (digitalRead(DIR_PIN) ? 1 : -1);
    } else {
        isMoving = false;
    }
}

void MotorDriver::toPosition(float pos, unsigned int feedrate) {
    unsigned long targetPulse = pos * STEP_PER_MM;
    long dPulse = (long) targetPulse - ABS_POS_PULSE + OFFSET_POS_PULSE;
    if (dPulse > 0) {
        forward(dPulse, feedrate);
    }
    else if (dPulse < 0)  {
        backward(dPulse, feedrate);         // TODO backward(-dPulse, feedrate)
    }
};

void MotorDriver::setCoordinate(float pos) {
    OFFSET_POS_PULSE = ABS_POS_PULSE - pos * STEP_PER_MM;
};

bool MotorDriver::isMovingMotor() {
    return isMoving;
}

void MotorDriver::invertDirection(){
    REVERT_CALIBRATE = !REVERT_CALIBRATE;
};

void MotorDriver::setEnable(bool en) {
    digitalWrite(EN_PIN, !en);
}
