/*
  The class we use to represent the ball bouncing around the screen. It's
  position and velocity can be modified freely by other entities.
*/


// Include guard
#ifndef BALL_H
#define BALL_H

// Required for types
#include "players.h"


namespace GameComponents {

  class Ball {
    public:
      // We need this constant for collision handling elsewhere
      static const uint8_t BALL_RADIUS;

      int8_t x;
      int8_t y;
      int8_t xDot;
      int8_t yDot;
      Ball(void);
      void reset(void);
      void tick(void);
      void render(void);
      Game::Player *roundWinner(void);
  };

}


#endif // Include guard
