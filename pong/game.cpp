/*
  Implementation file for the game. Really just orchestrates all the other sub-
  components.
*/


#include <Arduino.h>
#include "game.h"
#include "players.h"
#include "score.h"
#include "ball.h"
#include "paddles.h"
#include "io.h"


// Initialization code
// Again, Arduino doesn't take kindly to if we try to do everything in a
//  constructor, so have an init()

Game::GameModel::GameModel(void)
: score()
, ball()
, paddles() {
  // Can't do anything else here
  // Call init() in the main code
}

void Game::GameModel::init(void) {
  // Initialize IO
  IO::WN_LED.init();
  IO::LS_LED.init();
  IO::COLLISION_BUZZER.init();
  IO::UP_BUTTON.init();
  IO::DN_BUTTON.init();
  IO::I2C_DISPLAY.init();
}


void Game::GameModel::frame(void) {

  // Tick our components
  this->ball.tick();
  this->paddles.tick(&(this->ball));

  // Render everything out
  IO::I2C_DISPLAY.beginTransaction();
  this->score.render();
  this->ball.render();
  this->paddles.render();
  IO::I2C_DISPLAY.commitTransaction();

  // Handle round finishing
  // We do this last since it blocks
  Game::Player *winner = this->ball.roundWinner();
  if(winner != NULL) {
    // Flash the LED and increment score
    this->score.score(*winner);
    // Reset everything else
    this->ball.reset();
    this->paddles.reset();
  }
}
