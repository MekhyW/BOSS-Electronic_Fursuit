#include <Adafruit_NeoPixel.h>
#define LED_PIN 10
#define LED_COUNT 41
Adafruit_NeoPixel GearsStrip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
int Color_Brightness = 25;
uint32_t black = GearsStrip.Color(0, 0, 0);
uint32_t white = GearsStrip.Color(255, 255, 255);
uint32_t red = GearsStrip.Color(255, 0, 0);
uint32_t yellow = GearsStrip.Color(255, 255, 0);
uint32_t pink = GearsStrip.Color(255, 0, 255);
uint32_t deep_blue = GearsStrip.Color(0, 0, 255);
uint32_t light_blue = GearsStrip.Color(0, 255, 255);
uint32_t orange = GearsStrip.Color(255, 128, 0);
uint32_t green = GearsStrip.Color(0, 255, 0);
uint32_t purple = GearsStrip.Color(115, 0, 255);
int ExpressionState = 0;
int Effect = 1;
uint32_t* activeColor = &white;
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

void colorStatic(uint32_t color) {
  GearsStrip.setBrightness(Color_Brightness/2);
  GearsStrip.fill(color, 0, GearsStrip.numPixels());
  GearsStrip.show();
}

void colorSparkle(uint32_t color) {
  GearsStrip.setBrightness(Color_Brightness*3);
  int Pixel = random(GearsStrip.numPixels());
  GearsStrip.setPixelColor(Pixel, color);
  GearsStrip.show();
  delay(50);
  GearsStrip.setPixelColor(Pixel, black);
}

void colorTwinkle(uint32_t color) {
  GearsStrip.setBrightness(Color_Brightness*2);
  GearsStrip.fill(black, 0, GearsStrip.numPixels());
  for (int i=0; i<(GearsStrip.numPixels())/2; i++) {
     GearsStrip.setPixelColor(random(GearsStrip.numPixels()), color);
     GearsStrip.show();
     delay(100);
   }
  delay(100);
}

void colorStrobe(uint32_t color){
  GearsStrip.setBrightness(Color_Brightness);
  for(int j = 0; j < 10; j++) {
    int ExpressionStateLocal = ExpressionState;
    if(ExpressionState != ExpressionStateLocal){
      break;
    }
    GearsStrip.fill(color, 0, GearsStrip.numPixels());
    GearsStrip.show();
    delay(50);
    GearsStrip.fill(black, 0, GearsStrip.numPixels());
    GearsStrip.show();
    delay(50);
  }
 delay(1500);
}

void colorFade(uint32_t color){
    GearsStrip.setBrightness(Color_Brightness);
    for(int k = 0; k < Color_Brightness*2; k++) {
      int ExpressionStateLocal = ExpressionState;
      if(ExpressionState != ExpressionStateLocal){
        break;
      }
      GearsStrip.fill(color, 0, GearsStrip.numPixels());
      GearsStrip.setBrightness(k);
      GearsStrip.show();
      delay(25);
    }
    for(int k = Color_Brightness*2; k > 0; k--) {
      int ExpressionStateLocal = ExpressionState;
      if(ExpressionState != ExpressionStateLocal){
        break;
      }
      GearsStrip.fill(color, 0, GearsStrip.numPixels());
      GearsStrip.setBrightness(k);
      GearsStrip.show();
      delay(25);
    }
}

void colorWipe(uint32_t color) {
  GearsStrip.setBrightness(Color_Brightness);
  for(uint16_t i=0; i<GearsStrip.numPixels(); i++) {
    int ExpressionStateLocal = ExpressionState;
    if(ExpressionState != ExpressionStateLocal){
      break;
    }
    GearsStrip.setPixelColor(i, color);
    GearsStrip.show();
    delay(100);
  }
  for(uint16_t i=0; i<GearsStrip.numPixels(); i++) {
    int ExpressionStateLocal = ExpressionState;
    if(ExpressionState != ExpressionStateLocal){
      break;
    }
    GearsStrip.setPixelColor(i, black);
    GearsStrip.show();
    delay(100);
  }
}


void colorTheaterChase(uint32_t color) {
  GearsStrip.setBrightness(Color_Brightness*2);
  for(int a=0; a<10; a++) {
    for(int b=0; b<3; b++) {
      GearsStrip.clear();
      for(int c=b; c<GearsStrip.numPixels(); c += 3) {
        GearsStrip.setPixelColor(c, color);
      }
      int ExpressionStateLocal = ExpressionState;
      if(ExpressionState != ExpressionStateLocal){
        break;
      }
      GearsStrip.show();
      delay(200);
    }
  }
}

void Rainbow(int wait) {
  GearsStrip.setBrightness(Color_Brightness*2);
  for(long firstPixelHue = 0; firstPixelHue < 5*65536; firstPixelHue += 256) {
    for(int i=0; i<GearsStrip.numPixels(); i++) {
      int pixelHue = firstPixelHue + (i * 65536L / GearsStrip.numPixels());
      GearsStrip.setPixelColor(i, GearsStrip.gamma32(GearsStrip.ColorHSV(pixelHue)));
    }
    int ExpressionStateLocal = ExpressionState;
    if(ExpressionState != ExpressionStateLocal){
      break;
    }
    GearsStrip.show();
    delay(wait);
  }
}

void Off() {
  GearsStrip.fill(black, 0, GearsStrip.numPixels());
  GearsStrip.show();
}

void setup() {
  Serial.begin(9600);
  GearsStrip.begin();
  GearsStrip.show();
}

void loop() {
  readSerialPort();
  if (msg != msg_prev) {
    Effect = random(0, 8);
  }
  if (msg == "99") {
    Off();
  }
  else {
    if (msg == "0") {
      //neutral
      colorStatic(white);
    }
    else if (msg == "7") {
      //hypnotized
      Rainbow(10);
    }
    else {
      //cannot use switch case because it´s a String
      if (msg == "1" || msg == "8") {
        //angry or demonic
        activeColor = &red;
      }
      else if (msg == "2") {
        //disgusted
        activeColor = &green;
      }
      else if (msg == "3") {
        //sad
        activeColor = &deep_blue;
      }
      else if (msg == "4") {
        //happy
        activeColor = &yellow;
      }
      else if (msg == "5") {
        //scared
        activeColor = &purple;
      }
      else if (msg == "6") {
        //in love
        activeColor = &pink;
      }
      else {
        activeColor = &black;
      }
      switch(Effect){
          case 1:
            colorSparkle(*activeColor);
            break;
          case 2:
            colorTwinkle(*activeColor);
            break;
          case 3:
            colorStrobe(*activeColor);
            break;
          case 4:
            colorFade(*activeColor);
            break;
          case 5:
            colorWipe(*activeColor);
            break;
          case 6:
            colorTheaterChase(*activeColor);
            break;
        }
    }
  }
  delay(10);
}