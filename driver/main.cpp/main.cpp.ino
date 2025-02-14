// main.cpp.ino
#include "stepperMotorDriver.h"
#include "gcodeInterpreter.h"

MotorDriver motor1;
MotorDriver motor2;
GCodeInterpreter gcode(motor1, motor2);

void setup() {
  Serial.begin(115200);
  motor2.configure(2, 3, 4);  // Example pins for motor Y
  motor1.configure(5, 6, 7);  // Example pins for motor X
  motor1.setEnable(true);
  motor2.setEnable(true);
}

void loop() {
  // motor1.forward(200, 1200);  // Move motor 1 with 2000 pulses at feedrate 500

  // if (Serial.available()) {
  //   String command = Serial.readStringUntil('\n');
  //   gcode.parseCommand(command);
  // }



  if (!motor1.isMovingMotor() && !motor2.isMovingMotor()) {
    motor1.forward(100, 2000);  // Move motor 1 with 2000 pulses at feedrate 500
    motor2.forward(10, 200);    // Move motor 2 with 2000 pulses at feedrate 500
  }

  // delay(5000);
  motor1.stepNonBlocking();
  motor2.stepNonBlocking();
}
