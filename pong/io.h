/*
  This file the classes the program will use to interact with IO. We don't want
  to be touching it directly - hence this layer of abstraction.
*/


// Include guard
#ifndef IO_H
#define IO_H


// Required for Arduino stuff
#include <Arduino.h>
// Required for screen IO
#include <U8g2lib.h>


namespace IO {

    // Used for the LEDs that flash when the player wins or loses
    class AlertLED {
      private:
        uint32_t ledPin;
      public:
        AlertLED(const uint32_t pin);
        void init(void);
        void flash(void);
    };

    // Used for the buzzer that beeps when the ball collides with a wall
    class Buzzer {
      private:
        uint32_t buzzerPin;
      public:
        Buzzer(const uint32_t pin);
        void init(void);
        void beep(void);
    };

    // Used for the up and down buttons
    class Button {
      private:
        uint32_t buttonPin;
      public:
        Button(const uint32_t pin);
        void init(void);
        bool isPressed(void);
    };

    // A thin wrapper around U8g2 we use for drawing
    class Display {
      private:
        const uint32_t clockSpeed;
        const uint8_t *font;
      public:
        U8G2_SSD1327_MIDAS_128X128_F_HW_I2C canvas;
        Display(const uint32_t c, const u8g2_cb_t *r, const uint8_t *f);
        void init(void);
        void beginTransaction(void);
        void commitTransaction(void);
        void rollbackTransaction(void);
        void drawTest(void);
    };


    // Define the variables we will use to access our IO
    // These are all instances of the above classes
    extern AlertLED WN_LED;
    extern AlertLED LS_LED;
    extern Buzzer COLLISION_BUZZER;
    extern Button UP_BUTTON;
    extern Button DN_BUTTON;
    extern Display I2C_DISPLAY;

} // namespace IO

#endif // Include guard
