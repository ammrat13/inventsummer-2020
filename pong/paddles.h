/*
  A class we use to represent the paddles on either side of the arena. Note
  the we use one class to represent both paddles.
*/


// Include guard
#ifndef PADDLES_H
#define PADDLES_H


// Required for typing
#include "players.h"
#include "ball.h"


namespace GameComponents {

  class Paddles {
    private:
      int8_t paddleY[2];
    public:
      Paddles(void);
      void reset(void);
      void tick(GameComponents::Ball *b);
      void render(void);
  };

}


#endif // Include guard
