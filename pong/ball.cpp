/*
  Implementation file for the ball.
*/


#include <Arduino.h>
#include "players.h"
#include "ball.h"
#include "io.h"


// Constants for the ball
const uint8_t BALL_RADIUS = 10;


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
  // Also play a tone if we happen to get a collision
  // Start by flipping the coordinate system so the wall is at y=0
  // Note that we don't flip the velocity because we don't need to
  bool flip = this->yDot > 0;
  if(flip) {
    this->y = 127 - this->y;
  }
  // Do the collision check
  if(this->y < BALL_RADIUS) {
    this->y = 2*BALL_RADIUS - this->y;
    this->yDot *= -1;
    IO::COLLISION_BUZZER.beep();
  }
  // Flip back if we flipped the first time
  if(flip) {
    this->y = 127 - this->y;
  }
}


void GameComponents::Ball::render(void) {
  IO::I2C_DISPLAY.canvas.drawDisc(this->x, this->y, BALL_RADIUS);
}


// Check for win condition
// Null means noone has won yet
Game::Player *GameComponents::Ball::roundWinner(void) {
  if(this->x < 0) {
    if(this->xDot > 0) {
      return &Game::PLAYER_0;
    } else if(this->xDot < 0) {
      return &Game::PLAYER_1;
    }
  }
  return (Game::Player *const) NULL;
}
