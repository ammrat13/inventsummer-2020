/*
  A class that we use to keep track of and render the score. Note that
  rendering expects the display to already be initialized.
*/


// Include guard
#ifndef SCORE_H
#define SCORE_H

// Required for types and implementation
#include "game.h"
#include "io.h"


namespace GameComponents {

  // We store the scores in an array
  // Index 0 is Player 0, Index 1 is Player 1
  class Score {
    private:
      uint8_t scores[2];
    public:
      Score(void);
      void score(Game::Player player);
      void render(void);
  };

}


#endif // Include guard
