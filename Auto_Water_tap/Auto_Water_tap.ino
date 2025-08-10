#define trigPin 7
#define echoPin 6
#define pumpPin 9

long duration;
int distance;

unsigned long lastDetectedTime = 0;
const unsigned long offDelay = 5000;  // 5 seconds

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(pumpPin, OUTPUT);
  digitalWrite(pumpPin, LOW);  // Start with pump OFF
  Serial.begin(9600);
}

void loop() {
  // Trigger the ultrasonic pulse
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read echo time and convert to distance
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  // If hand is detected
  if (distance > 0 && distance <= 5) {
    digitalWrite(pumpPin, HIGH);           // Turn pump ON immediately
    lastDetectedTime = millis();           // Update time of last detection
  } else {
    // Check how long it's been since last detection
    if (millis() - lastDetectedTime > offDelay) {
      digitalWrite(pumpPin, LOW);          // Turn OFF pump after 5s
    }
  }

  delay(100);  // Small delay to avoid jitter
}
