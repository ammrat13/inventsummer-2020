/*
    This file the classes the program will use to interact with IO. We don't
    want to be touching it directly - hence this layer of abstraction.
*/


// Include guard
#ifndef IO_H
#define IO_H


// Required for Arduino stuff
#include <Arduino.h>
// Required for screen IO
#include <U8g2lib.h>


// Used for the LEDs that flash when the player wins or loses
class AlertLED {
  private:
    uint32_t ledPin;
  public:
    AlertLED(uint32_t pin);
    void flash();
    void clear();
};

// Used for the buzzer that beeps when the ball collides with a wall
class Buzzer {
  private:
    uint32_t buzzerPin;
  public:
    Buzzer(uint32_t pin);
    void beep();
};

// Used for the up and down buttons
class Button {
  private:
    uint32_t buttonPin;
  public:
    Button(uint32_t pin);
    bool isPressed();
};

// A thin wrapper around U8g2 we use for drawing
class Display {
  private:
    U8G2_SSD1327_MIDAS_128X128_F_HW_I2C u8g2;
  public:
    Display(uint32_t clockSpeed, const u8g2_cb_t *rot, const uint8_t *font);
    void commit();
    void drawTest();
};


// Define the variables we will use to access our IO
// These are all instances of the above classes
extern AlertLED wnLed;
extern AlertLED lsLed;
extern Buzzer collisionBuzzer;
extern Button upButton;
extern Button dnButton;
extern Display display;


// Include guard
#endif
