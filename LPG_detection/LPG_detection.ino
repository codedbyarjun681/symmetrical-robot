int gasSensorPin = A0;
int ledPin = 8;
int threshold = 280;  // Adjust based on calibration

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int gasValue = analogRead(gasSensorPin);
  Serial.println(gasValue);

  if (gasValue > threshold) {
    digitalWrite(ledPin, HIGH); // LPG detected
  } else {
    digitalWrite(ledPin, LOW);  // Safe
  }

  delay(500);
}
