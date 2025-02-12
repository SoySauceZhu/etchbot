#include "stepperMotorDriver.h"


MotorDriver mdX;
MotorDriver mdY;


void setup() {
  mdX.configure(2, 3, 4);
  mdY.configure(5, 6, 7);
}

void loop() {
  // md.forward(200, 60);
  mdX.setEnable(true);  // Enable Pin logic high to disable, logic low to enable
  mdY.setEnable(true);
  mdX.sendPulse(200, 600);
  mdY.sendPulse(200, 600);
}