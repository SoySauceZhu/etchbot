#include "gcodeInterpreter.h"

void GCodeInterpreter::parseCommand(String command) {

  command.trim();

  if (command.startsWith("QPos")) {
    Serial.print("Current ABS_POS_PULSE X: ");
    Serial.print(xMotor.getCurrentPosition());
    Serial.print(", Y: ");
    Serial.println(yMotor.getCurrentPosition());
  }

  if (command.startsWith("G0") || command.startsWith("G1")) {  // Linear move
    float x = 0, y = 0;
    int feedrate = 500;
    int xIndex = command.indexOf('X');
    int yIndex = command.indexOf('Y');
    int fIndex = command.indexOf('F');

    if (xIndex != -1) {
      x = command.substring(xIndex + 1).toFloat();
    }
    if (yIndex != -1) {
      y = command.substring(yIndex + 1).toFloat();
    }
    if (fIndex != -1) {
      feedrate = command.substring(fIndex + 1).toInt();
    }

    int xFeedrate = feedrate * x / sqrt(x * x + y * y);
    int yFeedrate = feedrate * y / sqrt(x * x + y * y);

    xMotor.toPosition(x, xFeedrate);
    yMotor.toPosition(y, yFeedrate);
  }
}
