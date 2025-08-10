#define CLK 2     // Clock pin
#define DT 3      // Data pin
#define SW 4      // Button pin

volatile int pulseCount = 0;
int lastEncoded = 0;
int zeroOffset = 0;  // To store the reference position when reset

const int pulsesPerRevolution = 20; // Change this to match your encoder

void setup() {
  pinMode(CLK, INPUT);
  pinMode(DT, INPUT);
  pinMode(SW, INPUT_PULLUP); // Enable internal pull-up resistor for the button

  attachInterrupt(digitalPinToInterrupt(CLK), updateEncoder, CHANGE);

  Serial.begin(9600);
}

void loop() {
  // Check if button is pressed
  if (digitalRead(SW) == LOW) {
    zeroOffset = pulseCount; // Set current position as zero
    Serial.println("Position Reset");
    delay(300); // Simple debounce delay
  }

  // Calculate angle relative to the new zero
  int relativeCount = pulseCount - zeroOffset;
  float angle = (relativeCount % pulsesPerRevolution) * (360.0 / pulsesPerRevolution);

  // Keep angle within 0–360 range
  if (angle < 0) angle += 360;

  Serial.print("Shaft Angle: ");
  Serial.print(angle);
  Serial.println("°");

  delay(100);
}

void updateEncoder() {
  int MSB = digitalRead(CLK); // Most significant bit
  int LSB = digitalRead(DT);  // Least significant bit

  int encoded = (MSB << 1) | LSB;
  int sum = (lastEncoded << 2) | encoded;

  if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) {
    pulseCount++;
  }
  if (sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) {
    pulseCount--;
  }

  lastEncoded = encoded;
}
