#include <DHT.h>

// Define DHT sensor type and pin
#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

// Define fan control pin
#define FANPIN 9

// Temperature thresholds
float T_low = 5.0;  // Low temperature threshold (°C)
float T_medium = 10.0; // Medium temperature threshold (°C)

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(FANPIN, OUTPUT);
}

void loop() {
  // Read temperature from DHT11
  float temp = dht.readTemperature();

  // Check if reading is valid
  if (isnan(temp)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Print temperature to Serial Monitor
  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.println(" °C");

  // Control fan speed based on temperature
  if (temp < T_low) {
    analogWrite(FANPIN, 0);  // Fan OFF
  } else if (temp >= T_low && temp < T_medium) {
    analogWrite(FANPIN, 128);  // Medium speed (50%)
  } else {
    analogWrite(FANPIN, 255);  // High speed (100%)
  }

  delay(1000);  // Delay 1 second between readings
}
