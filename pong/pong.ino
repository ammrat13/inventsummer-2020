#include "io.h"

void setup() {
  IO::I2C_DISPLAY.init();
}

void loop() {
  IO::I2C_DISPLAY.beginTransaction();
  IO::I2C_DISPLAY.canvas.drawStr(0,128,"HELLO");
  IO::I2C_DISPLAY.commitTransaction();
}
