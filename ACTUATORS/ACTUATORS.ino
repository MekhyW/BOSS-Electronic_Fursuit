#include <Servo.h>
#include <ros.h>
#include <std_msgs/UInt16.h>
#define randDisparityAvg 0
#define randTwitchDtAvg 0
#define randDurationAvg 0
#define randAngleAvg 0
#define randTwitchAngleAvg 0
#define LeftEyebrowPin 0
#define RightEyebrowPin 0
#define LeftEarPanPin 0
#define LeftEarTiltPin 0
#define RightEarPanPin 0
#define RightEarTiltPin 0
Servo LeftEyebrow;
Servo RightEyebrow;
Servo LeftEarPan;
Servo LeftEarTilt;
Servo RightEarPan;
Servo RightEarTilt;
int ExpressionState = 0;
int LeftEyebrowPos = 90;
int RightEyebrowPos = 90;
int LeftEarPanPos = 90;
int LeftEarTiltPos = 90;
int RightEarPanPos = 90;
int RightEarTiltPos = 90;
long int t1;
long randDisparity;
long randTwitchDt;
long randDuration;
long randAngle;
long randTwitchAngle;

void expressionCallback(std_msgs::UInt16& value){
  ExpressionState = value.data;
}
ros::NodeHandle nodehandle;
ros::Subscriber<std_msgs::UInt16> sub_expression("expression", &expressionCallback);

void stableMove(int ExpressionState) {
  switch(ExpressionState) {
    case 0:
      //neutral
      LeftEyebrowPos = 90;
      RightEyebrowPos = 90;
      LeftEarPanPos = 90;
      LeftEarTiltPos = 90;
      RightEarPanPos = 90;
      RightEarTiltPos = 90;
      break;
    case 1:
      //angry
      LeftEyebrowPos = 90;
      RightEyebrowPos = 90;
      LeftEarPanPos = 90;
      LeftEarTiltPos = 90;
      RightEarPanPos = 90;
      RightEarTiltPos = 90;
      break;
    case 2:
      //disgusted
      LeftEyebrowPos = 90;
      RightEyebrowPos = 90;
      LeftEarPanPos = 90;
      LeftEarTiltPos = 90;
      RightEarPanPos = 90;
      RightEarTiltPos = 90;
      break;
    case 3:
      //sad
      LeftEyebrowPos = 90;
      RightEyebrowPos = 90;
      LeftEarPanPos = 90;
      LeftEarTiltPos = 90;
      RightEarPanPos = 90;
      RightEarTiltPos = 90;
      break;
    case 4:
      //happy
      LeftEyebrowPos = 90;
      RightEyebrowPos = 90;
      LeftEarPanPos = 90;
      LeftEarTiltPos = 90;
      RightEarPanPos = 90;
      RightEarTiltPos = 90;
      break;
    case 5:
      //scared
      LeftEyebrowPos = 90;
      RightEyebrowPos = 90;
      LeftEarPanPos = 90;
      LeftEarTiltPos = 90;
      RightEarPanPos = 90;
      RightEarTiltPos = 90;
      break;
    case 6:
      //in love
      LeftEyebrowPos = 90;
      RightEyebrowPos = 90;
      LeftEarPanPos = 90;
      LeftEarTiltPos = 90;
      RightEarPanPos = 90;
      RightEarTiltPos = 90;
      break;
    case 7:
      //hypnotized
      LeftEyebrowPos = 90;
      RightEyebrowPos = 90;
      LeftEarPanPos = 90;
      LeftEarTiltPos = 90;
      RightEarPanPos = 90;
      RightEarTiltPos = 90;
      break;
    default:
      LeftEyebrowPos = 90;
      RightEyebrowPos = 90;
      LeftEarPanPos = 90;
      LeftEarTiltPos = 90;
      RightEarPanPos = 90;
      RightEarTiltPos = 90;
      break;
  }
  LeftEyebrow.write(LeftEyebrowPos);
  RightEyebrow.write(RightEyebrowPos);
  LeftEarPan.write(LeftEarPanPos);
  LeftEarTilt.write(LeftEarTiltPos);
  RightEarPan.write(RightEarPanPos);
  RightEarTilt.write(RightEarTiltPos);
}

void twitchPan(int target) {
  for (int n = 0; n < int(randDuration / randTwitchDt); n++) {
    if (target == 0 || target == 2)
      LeftEarPan.write(LeftEarPanPos + randTwitchAngle);
    if (target == 1 || target == 2)
      RightEarPan.write(RightEarPanPos - randTwitchAngle);
    delay(randTwitchDt/2);
    if (target == 0 || target == 2)
      LeftEarPan.write(LeftEarPanPos - randTwitchAngle);
    if (target == 1 || target == 2)
      RightEarPan.write(RightEarPanPos + randTwitchAngle);
    delay(randTwitchDt/2);
  }
}

void twitchTilt(int target) {
  for (int n = 0; n < int(randDuration / randTwitchDt); n++) {
    if (target == 0 || target == 2)
      LeftEarTilt.write(LeftEarTiltPos + randTwitchAngle);
    if (target == 1 || target == 2)
      RightEarTilt.write(RightEarTiltPos - randTwitchAngle);
    delay(randTwitchDt/2);
    if (target == 0 || target == 2)
      LeftEarTilt.write(LeftEarTiltPos - randTwitchAngle);
    if (target == 1 || target == 2)
      RightEarTilt.write(RightEarTiltPos + randTwitchAngle);
    delay(randTwitchDt/2);
  }
}

void sidewaysOut(int target) {
  if (target == 0 || target == 2)
    LeftEarPan.write(LeftEarPanPos - randAngle);
  if (target == 1 || target == 2)
    RightEarPan.write(RightEarPanPos + randAngle);
}

void sidewaysIn(int target) {
  if (target == 0 || target == 2)
    LeftEarPan.write(LeftEarPanPos + randAngle);
  if (target == 1 || target == 2)
    RightEarPan.write(RightEarPanPos - randAngle);
}

void perkUp(int target) {
  if (target == 0 || target == 2)
    LeftEarTilt.write(LeftEarTiltPos - randAngle);
  if (target == 1 || target == 2)
    RightEarTilt.write(RightEarTiltPos + randAngle);
}

void droop(int target) {
  if (target == 0 || target == 2)
    LeftEarTilt.write(LeftEarTiltPos + randAngle);
  if (target == 1 || target == 2)
    RightEarTilt.write(RightEarTiltPos - randAngle);
}

void randomMove(int move, int target) {
  switch (move) {
    case 0:
      twitchPan(target);
      break;
    case 1:
      twitchTilt(target);
      break;
    case 2:
      sidewaysOut(target);
      delay(randDuration);
      break;
    case 3:
      sidewaysIn(target);
      delay(randDuration);
      break;
    case 4:
      perkUp(target);
      delay(randDuration);
      break;
    case 5:
      droop(target);
      delay(randDuration);
      break;
    case 6:
      sidewaysOut(target);
      perkUp(target);
      delay(randDuration);
      break;
    case 7:
      sidewaysIn(target);
      perkUp(target);
      delay(randDuration);
      break;
    case 8:
      sidewaysOut(target);
      droop(target);
      delay(randDuration);
      break;
    case 9:
      sidewaysIn(target);
      droop(target);
      delay(randDuration);
      break;
    case 10:
      sidewaysOut(target);
      twitchTilt(target);
      break;
    case 11:
      sidewaysIn(target);
      twitchTilt(target);
      break;
    case 12:
      perkUp(target);
      twitchPan(target);
      break;
    case 13:
      droop(target);
      twitchPan(target);
      break;
    case 14:
      LeftEyebrow.write(LeftEyebrowPos + randAngle);
      RightEyebrow.write(RightEyebrowPos - randAngle);
      delay(randDuration);
      break;
    case 15:
      LeftEyebrow.write(LeftEyebrowPos - randAngle);
      RightEyebrow.write(RightEyebrowPos + randAngle);
      delay(randDuration);
      break;
    case 16:
      LeftEyebrow.write(LeftEyebrowPos - randAngle);
      RightEyebrow.write(RightEyebrowPos - randAngle);
      delay(randDuration);
      break;
    case 17:
      LeftEyebrow.write(LeftEyebrowPos + randAngle);
      RightEyebrow.write(RightEyebrowPos + randAngle);
      delay(randDuration);
      break;
  }
}

void updateRandTimes() {
  t1 = millis();
  randDisparity = random(randDisparityAvg/2, randDisparityAvg*2);
  randTwitchDt = random(randTwitchDtAvg/2, randTwitchDtAvg*2);
  randDuration = random(randDurationAvg/2, randDurationAvg*2);
  randAngle = random(randAngleAvg/2, randAngleAvg*2);
  randTwitchAngle = random(randTwitchAngleAvg/2, randTwitchAngleAvg*2);
}

void setup() {
  nodehandle.getHardware()->setBaud(115200);
  nodehandle.initNode();
  nodehandle.subscribe(sub_expression);
  LeftEyebrow.attach(LeftEyebrowPin);
  RightEyebrow.attach(RightEyebrowPin);
  LeftEarPan.attach(LeftEarPanPin);
  LeftEarTilt.attach(LeftEarTiltPin);
  RightEarPan.attach(RightEarPanPin);
  RightEarTilt.attach(RightEarTiltPin);
  updateRandTimes();
}

void loop() {
  stableMove(ExpressionState);
  if (millis() - t1 > randDisparity) {
    int move = random(18);
    int target = random(3);
    randomMove(move, target);
    updateRandTimes();
  }
  nodehandle.spinOnce();
}
