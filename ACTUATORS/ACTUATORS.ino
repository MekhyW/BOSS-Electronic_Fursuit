#include <Servo.h>
#define LeftEyebrowPin 11
#define RightEyebrowPin 10
#define LeftEyebrowDefault 90
#define RightEyebrowDefault 95
Servo LeftEyebrow;
Servo RightEyebrow;
int LeftEyebrowPos = LeftEyebrowDefault;
int RightEyebrowPos = RightEyebrowDefault;
int receivedValue = 0;
int receivedValue_prev = 0;

void Move(int receivedValue) {
  switch (receivedValue) {
    case 0:
    case 99:
      //Neutral
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 1:
      //Angry
      LeftEyebrowPos = LeftEyebrowDefault-50;
      RightEyebrowPos = RightEyebrowDefault+60;
      break;
    case 2:
      //Disgusted
      LeftEyebrowPos = LeftEyebrowDefault-25;
      RightEyebrowPos = RightEyebrowDefault+25;
      break;
    case 3:
      //Sad
      LeftEyebrowPos = LeftEyebrowDefault-25;
      RightEyebrowPos = RightEyebrowDefault+25;
      break;
    case 4:
      //Happy
      LeftEyebrowPos = LeftEyebrowDefault+30;
      RightEyebrowPos = RightEyebrowDefault-30;
      break;
    case 5:
      //Scared
      LeftEyebrowPos = LeftEyebrowDefault+15;
      RightEyebrowPos = RightEyebrowDefault-15;
      break;
    case 6:
      //Heart
      LeftEyebrowPos = LeftEyebrowDefault+30;
      RightEyebrowPos = RightEyebrowDefault-30;
      break;
    case 7:
      //Hypnotic
      LeftEyebrowPos = LeftEyebrowDefault-45;
      RightEyebrowPos = RightEyebrowDefault-30;
      break;
    case 8:
      //Sexy
      LeftEyebrowPos = LeftEyebrowDefault+30;
      RightEyebrowPos = RightEyebrowDefault+45;
      break;
    case 9:
      //Demonic
      LeftEyebrowPos = LeftEyebrowDefault-50;
      RightEyebrowPos = RightEyebrowDefault+60;
      break;
    default:
      return;
      break;
  }
  LeftEyebrow.attach(LeftEyebrowPin);
  RightEyebrow.attach(RightEyebrowPin);
  LeftEyebrow.write(LeftEyebrowPos);
  RightEyebrow.write(RightEyebrowPos);
  delay(700);
  LeftEyebrow.detach();
  RightEyebrow.detach();
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
  Move(0);
}

void loop() {
  readSerialPort();
  Serial.println(receivedValue);
  if (receivedValue != receivedValue_prev) {
    receivedValue_prev = receivedValue;
    Move(receivedValue); 
  }
  delay(10);
}
