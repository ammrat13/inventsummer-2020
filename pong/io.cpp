/*
  Implementation file for our IO library. It defines the methods given in all
  the classes, then calls the appropriate constructors.
*/

#include "io.h"


// Define the pins everything is on
// We don't do this in the constructor since we don't want everything to have
//  access and write to these.
// Note that pins 16 and 17 are swapped due to a bug
const uint32_t WN_LED_PIN = 1;
const uint32_t LS_LED_PIN = 2;
const uint32_t BUZZER_PIN = 7;
const uint32_t UP_BUTTON_PIN = 16;
const uint32_t DN_BUTTON_PIN = 17;
// Also define constants we use for the screen
const u8g2_cb_t *DISP_ROT = U8G2_R0;
const uint32_t DISP_CLOCK_SPEED = 1000000;
const uint8_t *DISP_FONT = u8g2_font_freedoomr10_mu;


// Implementation for AlertLED

IO::AlertLED::AlertLED(uint32_t pin)
: ledPin(pin) {
  // Rest of initialization done in init()
  // We have to do this because Arduino doesn't take kindly to constructors
}

void IO::AlertLED::init(void) {
  pinMode(this->ledPin, OUTPUT);
  digitalWrite(this->ledPin, LOW);
}

// Note that this function blocks
// We do this since we can't have multiple tone() at a time
void IO::AlertLED::flash(void) {
  const unsigned long TRANSITION_DELAY = 150;
  for(uint8_t i = 0; i < 4; i++) {
    digitalWrite(this->ledPin, HIGH);
    delay(TRANSITION_DELAY);
    digitalWrite(this->ledPin, LOW);
    delay(TRANSITION_DELAY);
  }
}


// Implementation for Buzzer

IO::Buzzer::Buzzer(uint32_t pin)
: buzzerPin(pin) {
  // Rest of initialization done in init()
  // We have to do this because Arduino doesn't take kindly to constructors
}

void IO::Buzzer::init(void) {
  pinMode(this->buzzerPin, OUTPUT);
}

void IO::Buzzer::beep(void) {
  tone(this->buzzerPin, 300, 200);
}


// Implementation for Button

IO::Button::Button(uint32_t pin)
: buttonPin(pin) {
  // Rest of initialization done in init()
  // We have to do this because Arduino doesn't take kindly to constructors
}

void IO::Button::init(void) {
  pinMode(this->buttonPin, INPUT_PULLUP);
}

bool IO::Button::isPressed(void) {
  return digitalRead(this->buttonPin) == LOW;
}


// Implementation for the display

IO::Display::Display(const uint32_t c, const u8g2_cb_t *r, const uint8_t *f)
: clockSpeed(c)
, font(f)
, canvas(r) {
  // Rest of initialization done in init()
  // We have to do this because Arduino doesn't take kindly to constructors
}

void IO::Display::init(void) {
  this->canvas.setBusClock(this->clockSpeed);
  this->canvas.begin();
}

void IO::Display::beginTransaction(void) {
  this->canvas.firstPage();
  this->canvas.setFont(this->font);
}

void IO::Display::commitTransaction(void) {
  this->canvas.nextPage();
}

void IO::Display::rollbackTransaction(void) {
  this->canvas.clear();
}


// Instantiate everything
IO::AlertLED IO::WN_LED(WN_LED_PIN);
IO::AlertLED IO::LS_LED(LS_LED_PIN);
IO::Buzzer IO::COLLISION_BUZZER(BUZZER_PIN);
IO::Button IO::UP_BUTTON(UP_BUTTON_PIN);
IO::Button IO::DN_BUTTON(DN_BUTTON_PIN);
IO::Display IO::I2C_DISPLAY(DISP_CLOCK_SPEED, DISP_ROT, DISP_FONT);
