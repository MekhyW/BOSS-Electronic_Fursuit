#include <Servo.h>
#include <ros.h>
#include <std_msgs/UInt16.h>
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

void expressionCallback(std_msgs::UInt16& value){
  ExpressionState = value.data;
}
ros::NodeHandle nodehandle;
ros::Subscriber<std_msgs::UInt16> sub_expression("expression", &expressionCallback);

void stableMove(int ExpressionState) {
  switch(ExpressionState) {
    case 0:
      //neutral
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 1:
      //angry
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 2:
      //disgusted
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 3:
      //sad
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 4:
      //happy
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 5:
      //scared
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 6:
      //in love
      LeftEyebrowPos = LeftEyebrowDefault;
      RightEyebrowPos = RightEyebrowDefault;
      break;
    case 7:
      //hypnotized
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

void randomMove(int move, int target) {
  switch (move) {
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
  nodehandle.getHardware()->setBaud(115200);
  nodehandle.initNode();
  nodehandle.subscribe(sub_expression);
  LeftEyebrow.attach(LeftEyebrowPin);
  RightEyebrow.attach(RightEyebrowPin);
  updateRandTimes();
}

void loop() {
  stableMove(ExpressionState);
  if (millis() - t1 > randDisparity) {
    randomMove(random(4));
    updateRandTimes();
  }
  nodehandle.spinOnce();
}
