#include "io.h"

void setup() {
  // Set the pin modes as appropriate
  pinMode(WN_LED_PIN, OUTPUT);
  pinMode(LS_LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(UP_BUT_PIN, INPUT_PULLUP);
  pinMode(DN_BUT_PIN, INPUT_PULLUP);

  SCREEN.setBusClock(1000000);
  SCREEN.begin();
  SCREEN.firstPage();
}

void loop() {
  digitalWrite(WN_LED_PIN, digitalRead(UP_BUT_PIN));
  SCREEN.setFont(u8g2_font_ncenB14_tr);
  SCREEN.drawStr(0,15,"Hello World!");
  SCREEN.nextPage();
}
