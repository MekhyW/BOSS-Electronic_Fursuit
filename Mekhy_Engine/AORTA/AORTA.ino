#include <Adafruit_NeoPixel.h>
#define LED_PIN 39
#define LED_COUNT 42
Adafruit_NeoPixel GearsStrip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
int ExpressionState = 0;
int Volume = 0;
byte inputarray[10];

void setup() {
  Serial.begin(9600);
  GearsStrip.begin();
  GearsStrip.show();
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
    if(inputarray[1] == 45){
      ExpressionState = inputarray[0]-48;
      if(inputarray[2] > 0 && inputarray[3] > 0 && inputarray[4] > 0){
        Volume = (100*(inputarray[2]-48)) + (10*(inputarray[3]-48)) + (inputarray[4]-48);
      } else if(inputarray[2] > 0 && inputarray[3] > 0 && inputarray[4] == 0){
        Volume = (10*(inputarray[2]-48)) + (inputarray[3]-48);
      } else if(inputarray[2] > 0 && inputarray[3] == 0 && inputarray[4] == 0){
        Volume = (inputarray[2]-48);
      }
    } else if(inputarray[2] == 45){
      ExpressionState = (10*(inputarray[0]-48)) + (inputarray[1]-48);
      if(inputarray[3] > 0 && inputarray[4] > 0 && inputarray[5] > 0){
        Volume = (100*(inputarray[3]-48)) + (10*(inputarray[4]-48)) + (inputarray[5]-48);
      } else if(inputarray[3] > 0 && inputarray[4] > 0 && inputarray[5] == 0){
        Volume = (10*(inputarray[3]-48)) + (inputarray[4]-48);
      } else if(inputarray[3] > 0 && inputarray[4] == 0 && inputarray[5] == 0){
        Volume = (inputarray[3]-48);
      }
    }
  }
  switch(ExpressionState){
    //cases
  }
  GearsStrip.show();
  Serial.print(ExpressionState);
  Serial.print("   ");
  Serial.println(Volume);
}
