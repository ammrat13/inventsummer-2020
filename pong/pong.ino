#include "io.h"

void setup() {
  display.init();
}

void loop() {
  display.beginTransaction();
  display.drawTest();
  display.commitTransaction();
}
