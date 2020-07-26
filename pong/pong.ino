/*
  The main file that initializes and runs the game.
*/


#include "game.h"

Game::GameModel game;

void setup() {
  game.init();
}

void loop() {
  game.frame();
}
