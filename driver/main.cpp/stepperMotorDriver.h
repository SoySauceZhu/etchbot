// stepperMotorDriver.h
#ifndef MOTOR_DRIVER_H
#define MOTOR_DRIVER_H
#include <Arduino.h>

class MotorDriver {
public:
  MotorDriver()
    : isMoving(false), lastStepTime(0), pulsesRemaining(0), stepDelay(0){};
  ~MotorDriver(){};

  void configure(short en, short step, short dir);
  void forward(unsigned long pulse, unsigned int feedrate);
  void backward(unsigned long pulse, unsigned int feedrate);
  void toPosition(float pos, unsigned int feedrate);  // Revised
  void stepNonBlocking();  // Non-blocking stepping function
  void setEnable(bool en);
  bool isMovingMotor();  // Checks if the motor is still moving
  void setCoordinate(float pos);
  void invertDirection();
  void toOrigin();
  void sendPulse(unsigned long pulse, unsigned int delay);
  long getCurrentPosition();


private:
  short EN_PIN;
  short STEP_PIN;
  short DIR_PIN;
  unsigned long ABS_POS_PULSE;
  unsigned long OFFSET_POS_PULSE;
  unsigned int STEP_PER_MM = 5;
  bool REVERT_CALIBRATE = 1;

  // Variables for non-blocking step execution
  bool isMoving;
  unsigned long lastStepTime;
  unsigned long pulsesRemaining;
  unsigned int stepDelay;
};

#endif
