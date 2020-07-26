/*
  The main file that initializes and runs the game.
*/


#include "io.h"
#include "paddles.h"


GameComponents::Paddles p;

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
  p.tick(NULL);
  IO::I2C_DISPLAY.beginTransaction();
  p.render();
  IO::I2C_DISPLAY.commitTransaction();
}
