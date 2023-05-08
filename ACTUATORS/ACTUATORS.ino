#include <Servo.h>
#define LeftEyebrowPin 2
#define RightEyebrowPin 3
#define LeftEyebrowDefault 90
#define RightEyebrowDefault 90
Servo LeftEyebrow;
Servo RightEyebrow;
int ExpressionState = 0;
int LeftEyebrowPos = LeftEyebrowDefault;
int RightEyebrowPos = RightEyebrowDefault;
int receivedValue = 0;
int receivedValue_prev = 0;

void Move(int receivedValue) {
  switch (receivedValue) {
    case 0:
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 1:
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 2:
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 3:
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 4:
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 5:
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 6:
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 7:
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    default:
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
  }
  LeftEyebrow.write(LeftEyebrowPos);
  RightEyebrow.write(RightEyebrowPos);
}

void readSerialPort() {
  if (Serial.available()) {
    receivedValue_prev = receivedValue;
    receivedValue = Serial.parseInt();
    Serial.flush();
  }
}

void setup() {
  Serial.begin(9600);
  LeftEyebrow.attach(LeftEyebrowPin);
  RightEyebrow.attach(RightEyebrowPin);
}

void loop() {
  readSerialPort();
  if (receivedValue != 99) {
    Move(receivedValue);
  } 
  else {
    LeftEyebrow.write(LeftEyebrowDefault);
    RightEyebrow.write(RightEyebrowDefault);
  }
  delay(10);
}
