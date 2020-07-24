// Define the pins we have IO on
#define WN_LED_PIN (1)
#define LS_LED_PIN (2)
#define BUZZER_PIN (7)
#define UP_BUT_PIN (16)
#define DN_BUT_PIN (17)


void setup() {
  // Set the pin modes as appropriate
  pinMode(WN_LED_PIN, OUTPUT);
  pinMode(LS_LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(UP_BUT_PIN, INPUT_PULLUP);
  pinMode(DN_BUT_PIN, INPUT_PULLUP);

  // Write stuff so we know it's working
  digitalWrite(WN_LED_PIN, HIGH);
  digitalWrite(LS_LED_PIN, HIGH);
  tone(BUZZER_PIN, 500);
}

void loop() {}
