#include <Servo.h>
#define LeftEyebrowPin 10
#define RightEyebrowPin 11
Servo LeftEyebrow;
Servo RightEyebrow;
int ExpressionState = 0;
byte inputarray[10];

void setup() {
  Serial.begin(9600);
  LeftEyebrow.attach(LeftEyebrowPin);
  RightEyebrow.attach(RightEyebrowPin);
}

void loop() {
  for (int x = 0; x < sizeof(inputarray) / sizeof(inputarray[0]); x++){
    inputarray[x] = 0;
  }
  Serial.flush();
  if(Serial.available()){
    Serial.readBytesUntil('\n', inputarray, sizeof(inputarray));
    while(Serial.available() > 0){
      Serial.read();
    }
    if(inputarray[1] == 0){
      ExpressionState = inputarray[0]-48;
    } else {
      ExpressionState = (10*(inputarray[0]-48)) + (inputarray[1]-48);
    }
  }
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
}
