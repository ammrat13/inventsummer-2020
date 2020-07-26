/*
  A file defining our model of the game, as well as other useful constants and
  methods.
*/


// Include guard
#ifndef GAME_H
#define GAME_H


#include "players.h"
#include "score.h"
#include "ball.h"
#include "paddles.h"


namespace Game {

  class GameModel {
    private:
      GameComponents::Score score;
      GameComponents::Ball ball;
      GameComponents::Paddles paddles;
    public:
      GameModel(void);
      void init(void);
      void frame(void);
  };

}

#endif // Include guard
