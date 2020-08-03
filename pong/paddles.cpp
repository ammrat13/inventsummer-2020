/*
  Implementation file for the paddles.
*/


#include <Arduino.h>
#include "players.h"
#include "paddles.h"
#include "ball.h"
#include "io.h"


// Constants for the paddles
const uint8_t PADDLE_HALF_HEIGHT = 10;
const uint8_t PADDLE_WIDTH = 2;
const uint8_t PADDLE_SPEED = 5;


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
  int8_t newY = paddleY[p] + d * PADDLE_SPEED;
  if(newY < PADDLE_HALF_HEIGHT || newY > 127 - PADDLE_HALF_HEIGHT) {
    if(d == UP) {
      newY = PADDLE_HALF_HEIGHT;
    } else if (d == DN) {
      newY = 127 - PADDLE_HALF_HEIGHT;
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

  // AI
  if(b->y < paddleY[Game::PLAYER_1]) {
    movePlayer(this->paddleY, Game::PLAYER_1, UP);
  } else {
    movePlayer(this->paddleY, Game::PLAYER_1, DN);
  }

  // Check for collision with the active paddle
  // Flip the coordinate system first if needed
  bool flip = b->xDot > 0;
  if(flip) {
    b->x = -b->x + 127;
    b->xDot *= -1;
  }
  // Do collision detection if needed
  if(b->x < PADDLE_WIDTH + GameComponents::Ball::BALL_RADIUS) {
    // Approximate the position of the ball at the time of collision
    // We don't want to use floats
    int8_t bY = b->y - b->yDot / 2;
    // Get the position of the active paddle at the time of the collision
    int8_t pY = paddleY[flip ? Game::PLAYER_1 : Game::PLAYER_0];
    // Ensure we were in range for the collision
    if(abs(bY - pY) <= PADDLE_HALF_HEIGHT + GameComponents::Ball::BALL_RADIUS) {
      // Set the position and velocity of the ball
      b->x = 2*PADDLE_WIDTH + 2*GameComponents::Ball::BALL_RADIUS - b->x;
      b->xDot *= -1;
      // Beep the buzzer
      IO::COLLISION_BUZZER.beep();
    }
  }
  // Flip back if we flipped
  if(flip) {
    b->x = -b->x + 127;
    b->xDot *= -1;
  }
}


void GameComponents::Paddles::render(void) {
  // Draw both P0 and P1's
  IO::I2C_DISPLAY.canvas.drawFrame(
    0,
    paddleY[0] - PADDLE_HALF_HEIGHT,
    PADDLE_WIDTH,
    2 * PADDLE_HALF_HEIGHT
  );
  IO::I2C_DISPLAY.canvas.drawFrame(
    128 - PADDLE_WIDTH,
    paddleY[1] - PADDLE_HALF_HEIGHT,
    PADDLE_WIDTH,
    2 * PADDLE_HALF_HEIGHT
  );
}
