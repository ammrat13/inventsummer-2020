/*
  Implementation file for the ball.
*/


#include <Arduino.h>
#include "players.h"
#include "ball.h"
#include "io.h"


// Constants for the ball
const uint8_t BALL_RADIUS = 2;


// Handlers for initialization

GameComponents::Ball::Ball(void) {
  this->reset();
}

void GameComponents::Ball::reset(void) {
  // Center the ball on screen
  this->x = 64;
  this->y = 64;
  // Start moving toward the player at an angle
  this->xDot = -3;
  this->yDot = -5;
}


void GameComponents::Ball::tick(void) {
  // Take a step in the direction we're going
  this->x += this->xDot;
  this->y += this->yDot;
  // Keep ourselves in bounds on y
  // Also play a tone on collission
  if(this->y < 0) {
    // Use bitwise not instead of negation for coordinate so we can guarantee
    //  the result to be non-negative
    this->y = ~this->y;
    this->yDot *= -1;
    IO::COLLISION_BUZZER.beep();
  }
  // Clamp the x to the edges to check for loss
  if(this->x < 0) {
    if(this->xDot < 0) {
      this->x = 0;
    } else {
      this->x = 127;
    }
  }
}


void GameComponents::Ball::render(void) {
  IO::I2C_DISPLAY.canvas.drawDisc(this->x, this->y, BALL_RADIUS);
}


// Check for win condition
// Null means noone has won yet
Game::Player *GameComponents::Ball::roundWinner(void) {
  if(this->x == 127) {
    return &Game::PLAYER_0;
  } else if(this->x == 0) {
    return &Game::PLAYER_1;
  } else {
    return (Game::Player *const) NULL;
  }
}
