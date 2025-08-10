#define LDR_PIN 2   // LDR module digital output
#define LED_PIN 8   // LED connected to pin 8

void setup() {
  pinMode(LDR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int ldrStatus = digitalRead(LDR_PIN);

  if (ldrStatus == LOW) { // It's dark
    digitalWrite(LED_PIN, LOW); // Turn on street light
  } else {
    digitalWrite(LED_PIN, HIGH); // Turn off street light
  }

  delay(100); // Small delay for stability
}
