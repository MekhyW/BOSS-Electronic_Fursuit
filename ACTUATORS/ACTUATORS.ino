#include <Servo.h>
#define LeftEyebrowPin 2
#define RightEyebrowPin 3
#define LeftEyebrowDefault 90
#define RightEyebrowDefault 90
Servo LeftEyebrow;
Servo RightEyebrow;
int LeftEyebrowPos = LeftEyebrowDefault;
int RightEyebrowPos = RightEyebrowDefault;
int receivedValue = 0;

void Move(int receivedValue) {
  switch (receivedValue) {
    case 0:
      //Neutral
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 1:
      //Angry
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 2:
      //Disgusted
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 3:
      //Sad
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 4:
      //Happy
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 5:
      //Scared
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 6:
      //Heart
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 7:
      //Hypnotic
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 8:
      //Sexy
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 9:
      //Demonic
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    default:
      break;
  }
  LeftEyebrow.write(LeftEyebrowPos);
  RightEyebrow.write(RightEyebrowPos);
}

void readSerialPort() {
  if (Serial.available()) {
    receivedValue = Serial.parseInt();
    Serial.flush();
  }
  while (Serial.available()){
    Serial.read();
  }
}

void setup() {
  Serial.begin(9600);
  LeftEyebrow.attach(LeftEyebrowPin);
  RightEyebrow.attach(RightEyebrowPin);
}

void loop() {
  readSerialPort();
  Serial.println(receivedValue);
  if (receivedValue != 99) {
    Move(receivedValue);
  } 
  else {
    LeftEyebrow.write(LeftEyebrowDefault);
    RightEyebrow.write(RightEyebrowDefault);
  }
  delay(10);
}
