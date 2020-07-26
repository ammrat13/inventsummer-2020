/*
  Implementation file for the score class.
*/


#include <Arduino.h>
#include "game.h"
#include "score.h"
#include "io.h"


GameComponents::Score::Score(void) {
  // Just initialize the current scores
  this->scores[Game::PLAYER_0] = 0;
  this->scores[Game::PLAYER_1] = 0;
}


// Note that, when a player scores, we block
// This is because flashing an LED blocks
void GameComponents::Score::score(Game::Player player) {
  // Flash the right LED
  if(player == Game::PLAYER_0) {
    IO::WN_LED.flash();
  } else if (player == Game::PLAYER_1) {
    IO::LS_LED.flash();
  }
  // Increment the score
  this->scores[player]++;
}



// Utility method for render()
// Takes a number and converts its least significant four bits to hex
char toHexChar(uint8_t n) {
  // Only consider the least significant four bits
  n &= 0xf;
  // Conversion logic
  if(n >= 10) {
    return n - 10 + 'A';
  } else {
    return n + '0';
  }
}

// Render to the screen
void GameComponents::Score::render(void) {
  // Convert the scores to hex strings
  char scoresStr[2][4];
  for(uint8_t i = 0; i < 2; i++) {
    // Null terminators
    scoresStr[i][2] = 0;
    // Less significant nibble
    scoresStr[i][1] = toHexChar(this->scores[i]);
    // More significant nibble
    // Special handling for zero
    scoresStr[i][0] = toHexChar(this->scores[i] >> 4);
    if(scoresStr[i][0] == '0') {
      scoresStr[i][0] = ' ';
    }
  }

  // Write to the screen
  IO::I2C_DISPLAY.canvas.drawStr(34, 20, scoresStr[Game::PLAYER_0]);
  IO::I2C_DISPLAY.canvas.drawStr(72, 20, scoresStr[Game::PLAYER_1]);
}
