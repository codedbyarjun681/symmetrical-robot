// Arduino L298N serial bridge
const int IN1 = 2;
const int IN2 = 3;
const int ENA = 5; // PWM
const int IN3 = 4;
const int IN4 = 7;
const int ENB = 6; // PWM

void setup() {
  Serial.begin(115200);
  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT); pinMode(ENB, OUTPUT);
  // set stopped
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
  analogWrite(ENA, 0); analogWrite(ENB, 0);
}

void setMotor(int pwmPin, int inA, int inB, int value) {
  // value: -255 .. 255
  int mag = abs(value);
  if (mag > 255) mag = 255;
  if (value > 0) {
    digitalWrite(inA, HIGH);
    digitalWrite(inB, LOW);
  } else if (value < 0) {
    digitalWrite(inA, LOW);
    digitalWrite(inB, HIGH);
  } else {
    // brake or float? use brake (both HIGH) or float (both LOW). We'll brake:
    digitalWrite(inA, HIGH);
    digitalWrite(inB, HIGH);
  }
  analogWrite(pwmPin, mag);
}

void loop() {
  static String buffer = "";
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      // parse line e.g. "L:120,R:-80"
      int L = 0, R = 0;
      int li = buffer.indexOf("L:");
      int ri = buffer.indexOf("R:");
      if (li != -1 && ri != -1) {
        String ls = buffer.substring(li+2, buffer.indexOf(',', li));
        String rs = buffer.substring(ri+2);
        L = ls.toInt();
        R = rs.toInt();
        // clamp -255..255
        if (L > 255) L = 255; if (L < -255) L = -255;
        if (R > 255) R = 255; if (R < -255) R = -255;
        setMotor(ENA, IN1, IN2, L);
        setMotor(ENB, IN3, IN4, R);
      }
      buffer = "";
    } else {
      buffer += c;
      // avoid runaway
      if (buffer.length() > 100) buffer = "";
    }
  }
}