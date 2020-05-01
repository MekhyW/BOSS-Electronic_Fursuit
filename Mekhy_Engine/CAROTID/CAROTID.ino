#include <Servo.h>
#define LeftEyebrowPin 0
#define RightEyebrowPin 0
Servo LeftEyebrow;
Servo RightEyebrow;
int ExpressionState = 0;
byte inputarray[10];

void setup() {
  Serial.begin(9600);
  LeftEyebrow.attach(LeftEyebrowPin);
  RightEyebrow.attach(RightEyebrowPin);
  LeftEyebrow.write(90);
  RightEyebrow.write(90);
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
    if(inputarray[1] != 0){
      ExpressionState = ((inputarray[0]-48)*10) + (inputarray[1]-48);
    } else {
      ExpressionState = (inputarray[0]-48);
    }
  }
  switch(ExpressionState){
    case 0:
      LeftEyebrow.write(90);
      RightEyebrow.write(90);
      break;
    case 1:
      LeftEyebrow.write(90);
      RightEyebrow.write(90);
      break;
    case 2:
      LeftEyebrow.write(90);
      RightEyebrow.write(90);
      break;
    case 3:
      LeftEyebrow.write(90);
      RightEyebrow.write(90);
      break;
    case 4:
      LeftEyebrow.write(90);
      RightEyebrow.write(90);
      break;
    case 5:
      LeftEyebrow.write(90);
      RightEyebrow.write(90);
      break;
    case 6:
      LeftEyebrow.write(90);
      RightEyebrow.write(90);
      break;
    case 7:
      LeftEyebrow.write(90);
      RightEyebrow.write(90);
      break;
    case 8:
      LeftEyebrow.write(90);
      RightEyebrow.write(90);
      break;
    case 9:
      LeftEyebrow.write(90);
      RightEyebrow.write(90);
      break;
    case 10:
      LeftEyebrow.write(90);
      RightEyebrow.write(90);
      break;
    case 11:
      LeftEyebrow.write(90);
      RightEyebrow.write(90);
      break;
    case 12:
      LeftEyebrow.write(90);
      RightEyebrow.write(90);
      break;
    case 13:
      LeftEyebrow.write(90);
      RightEyebrow.write(90);
      break;
    case 14:
      LeftEyebrow.write(90);
      RightEyebrow.write(90);
      break;
  }
}
