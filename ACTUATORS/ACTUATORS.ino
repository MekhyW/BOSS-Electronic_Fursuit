#include <Servo.h>
#define randDisparityAvg 0
#define randDurationAvg 0
#define randAngleAvg 0
#define LeftEyebrowPin 2
#define RightEyebrowPin 3
Servo LeftEyebrow;
Servo RightEyebrow;
#define LeftEyebrowDefault 90
#define RightEyebrowDefault 90
int ExpressionState = 0;
int LeftEyebrowPos = LeftEyebrowDefault;
int RightEyebrowPos = RightEyebrowDefault;
long int t1;
long randDisparity;
long randDuration;
long randAngle;
String msg = "";
String msg_prev = "";

void readSerialPort() {
  msg_prev = msg;
  msg = "";
  if (Serial.available()) {
    delay(10);
    while (Serial.available() > 0) {
      msg += (char)Serial.read();
    }
    Serial.flush();
  }
}

void stableMove(String msg) {
  //cannot use switch case because it´s a String
  if (msg == "0") {
    //neutral
    LeftEyebrowPos = LeftEyebrowDefault;
    RightEyebrowPos = RightEyebrowDefault;
  }
  if (msg == "1") {
    //angry
    LeftEyebrowPos = LeftEyebrowDefault;
    RightEyebrowPos = RightEyebrowDefault;
  }
  if (msg == "2") {
    //disgusted
    LeftEyebrowPos = LeftEyebrowDefault;
    RightEyebrowPos = RightEyebrowDefault;
  }
  if (msg == "3") {
    //sad
    LeftEyebrowPos = LeftEyebrowDefault;
    RightEyebrowPos = RightEyebrowDefault;
  }
  if (msg == "4") {
    //happy
    LeftEyebrowPos = LeftEyebrowDefault;
    RightEyebrowPos = RightEyebrowDefault;
  }
  if (msg == "5") {
    //scared
    LeftEyebrowPos = LeftEyebrowDefault;
    RightEyebrowPos = RightEyebrowDefault;
  }
  if (msg == "6") {
    //in love
    LeftEyebrowPos = LeftEyebrowDefault;
    RightEyebrowPos = RightEyebrowDefault;
  }
  if (msg == "7") {
    //hypnotic
    LeftEyebrowPos = LeftEyebrowDefault;
    RightEyebrowPos = RightEyebrowDefault;
  }
  else {
    LeftEyebrowPos = LeftEyebrowDefault;
    RightEyebrowPos = RightEyebrowDefault;
  }
  LeftEyebrow.write(LeftEyebrowPos);
  RightEyebrow.write(RightEyebrowPos);
}

void randomMove(int movement) {
  switch (movement) {
    case 0:
      LeftEyebrow.write(LeftEyebrowPos + randAngle);
      RightEyebrow.write(RightEyebrowPos - randAngle);
      delay(randDuration);
      break;
    case 1:
      LeftEyebrow.write(LeftEyebrowPos - randAngle);
      RightEyebrow.write(RightEyebrowPos + randAngle);
      delay(randDuration);
      break;
    case 2:
      LeftEyebrow.write(LeftEyebrowPos - randAngle);
      RightEyebrow.write(RightEyebrowPos - randAngle);
      delay(randDuration);
      break;
    case 3:
      LeftEyebrow.write(LeftEyebrowPos + randAngle);
      RightEyebrow.write(RightEyebrowPos + randAngle);
      delay(randDuration);
      break;
  }
}

void updateRandTimes() {
  t1 = millis();
  randDisparity = random(randDisparityAvg/2, randDisparityAvg*2);
  randDuration = random(randDurationAvg/2, randDurationAvg*2);
  randAngle = random(randAngleAvg/2, randAngleAvg*2);
}

void setup() {
  Serial.begin(9600);
  LeftEyebrow.attach(LeftEyebrowPin);
  RightEyebrow.attach(RightEyebrowPin);
  updateRandTimes();
}

void loop() {
  if (msg != "99") {
    stableMove(msg);
    if (millis() - t1 > randDisparity) {
      randomMove(random(4));
      updateRandTimes();
    }
  } 
  else {
    LeftEyebrow.write(LeftEyebrowDefault);
    RightEyebrow.write(RightEyebrowDefault);
  }
  delay(10);
}
