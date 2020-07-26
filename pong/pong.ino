/*
  The main file that initializes and runs the game.
*/


#include "io.h"
#include "score.h"


GameComponents::Score s;

void setup() {
  // Initialize all the IO
  // We can't do this in constructors
  IO::WN_LED.init();
  IO::LS_LED.init();
  IO::COLLISION_BUZZER.init();
  IO::UP_BUTTON.init();
  IO::DN_BUTTON.init();
  IO::I2C_DISPLAY.init();
}


void loop() {
  s.score(0);
  s.score(1);
  IO::I2C_DISPLAY.beginTransaction();
  s.render();
  IO::I2C_DISPLAY.commitTransaction();
}
