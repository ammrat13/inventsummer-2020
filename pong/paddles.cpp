/*
  Implementation file for the paddles.
*/


#include <Arduino.h>
#include "game.h"
#include "paddles.h"
#include "ball.h"
#include "io.h"


// Constants for the paddles
const uint8_t PADDLE_RADIUS = 8;
const uint8_t PADDLE_WIDTH = 3;


// Initialization

GameComponents::Paddles::Paddles(void) {
  this->reset();
}

void GameComponents::Paddles::reset(void) {
  this->paddleY[Game::PLAYER_0] = 64;
  this->paddleY[Game::PLAYER_1] = 64;
}


// Helper function for tick()
// Moves the specified player's paddle up or down, depending on the constant
// Note that it takes in a parameter of y values to read and modify
typedef int8_t MoveDirection;
const MoveDirection UP = -1;
const MoveDirection DN = 1;
void movePlayer(int8_t *paddleY, Game::Player p, MoveDirection d) {
  // Compute the new position after stepping the specified amount
  int8_t newY = paddleY[p] + d * 7;
  if(newY < PADDLE_RADIUS || newY > 127 - PADDLE_RADIUS) {
    if(d == UP) {
      newY = PADDLE_RADIUS;
    } else if (d == DN) {
      newY = 127 - PADDLE_RADIUS;
    }
  }
  // Assign
  paddleY[p] = newY;
}

void GameComponents::Paddles::tick(GameComponents::Ball *b) {

  // Move the player's paddle
  // Note that we don't use else-if. If the player is pressing both buttons, we
  //  want nothing to happen overall.
  if(IO::UP_BUTTON.isPressed()) {
    movePlayer(this->paddleY, Game::PLAYER_0, UP);
  }
  if(IO::DN_BUTTON.isPressed()) {
    movePlayer(this->paddleY, Game::PLAYER_0, DN);
  }
}


void GameComponents::Paddles::render(void) {
  // Draw both P0 and P1's
  IO::I2C_DISPLAY.canvas.drawBox(
    0,
    paddleY[0] - PADDLE_RADIUS,
    PADDLE_WIDTH,
    2 * PADDLE_RADIUS
  );
  IO::I2C_DISPLAY.canvas.drawBox(
    127 - PADDLE_WIDTH,
    paddleY[1] - PADDLE_RADIUS,
    PADDLE_WIDTH,
    2 * PADDLE_RADIUS
  );
}
