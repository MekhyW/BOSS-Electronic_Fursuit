#include <Servo.h>
#include <ros.h>
#include <std_msgs/UInt16.h>
#define LeftEyebrowPin 10
#define RightEyebrowPin 11
Servo LeftEyebrow;
Servo RightEyebrow;
int ExpressionState = 0;

void expressionCallback(std_msgs::UInt16& value){
  ExpressionState = value.data;
}
ros::NodeHandle nodehandle;
ros::Subscriber<std_msgs::UInt16> sub_expression("expression", &expressionCallback);

void setup() {
  Serial.begin(9600);
  LeftEyebrow.attach(LeftEyebrowPin);
  RightEyebrow.attach(RightEyebrowPin);
}

void loop() {
  switch(ExpressionState){
    case 0:
      LeftEyebrow.write(75);
      RightEyebrow.write(90);
      break;
    case 1:
      LeftEyebrow.write(110);
      RightEyebrow.write(55);
      break;
    case 2:
      //maintain
      break;
    case 3:
      LeftEyebrow.write(15);
      RightEyebrow.write(160);
      break;
    case 4:
      LeftEyebrow.write(55);
      RightEyebrow.write(110);
      break;
    case 5:
      LeftEyebrow.write(30);
      RightEyebrow.write(55);
      break;
    case 6:
      LeftEyebrow.write(55);
      RightEyebrow.write(110);
      break;
    case 7:
      LeftEyebrow.write(15);
      RightEyebrow.write(160);
      break;
    case 8:
      LeftEyebrow.write(65);
      RightEyebrow.write(100);
      break;
    case 9:
      LeftEyebrow.write(15);
      RightEyebrow.write(160);
      break;
    case 10:
      LeftEyebrow.write(105);
      RightEyebrow.write(60);
      break;
  }
  Serial.println(ExpressionState);
  nodehandle.spinOnce();
}
