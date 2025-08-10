// Pin Definitions
const int soilMoisturePin = A0; // Analog pin connected to sensor output
const int pumpControlPin = 8;   // Digital pin to control the MOSFET gate

// Moisture Threshold
// Lower values = drier soil. Tune this based on your sensor readings.
const int moistureThreshold = 1020;

void setup() {
  pinMode(pumpControlPin, OUTPUT); // Set pump control pin as output
  digitalWrite(pumpControlPin, LOW); // Make sure pump is off at start
  Serial.begin(9600); // Initialize serial monitor for debugging
}

void loop() {
  int moistureValue = analogRead(soilMoisturePin); // Read analog value from sensor

  // Print moisture value to Serial Monitor
  Serial.print("Soil Moisture Reading: ");
  Serial.println(moistureValue);

  // Compare with threshold
  if (moistureValue < moistureThreshold) {
    digitalWrite(pumpControlPin, LOW); // Soil is dry: turn ON pump
    Serial.println("Pump OFF");
  } else {
    digitalWrite(pumpControlPin, HIGH);  // Soil is wet: turn OFF pump
    Serial.println("Pump ON");
  }

  delay(1000); // Wait 1 second before next reading
}
