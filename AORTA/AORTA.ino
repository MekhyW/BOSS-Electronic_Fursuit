#include <Adafruit_NeoPixel.h>
#define LED_PIN 39
#define LED_COUNT 42
Adafruit_NeoPixel GearsStrip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
int PixelHeight[42] = {25, 27, 29, 31, 33, 32, 30, 28, 26, 24, 22, 19, 17, 16, 18, 21, 23, 20, 15, 12, 9, 7, 7, 9, 12, 15, 20, 22, 23, 23, 22, 10, 13, 14, 11, 8, 5, 2, 4, 6};
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
int ExpressionState = 0;
int Effect = 1;
byte inputarray[10];

void GetData(){
  for (int x = 0; x < sizeof(inputarray) / sizeof(inputarray[0]); x++){
    inputarray[x] = 0;
  }
  Serial.flush();
  if(Serial.available()){
    Serial.readBytesUntil('\n', inputarray, sizeof(inputarray));
    while(Serial.available() > 0){
      Serial.read();
    }
    int ExpressionStateLocal = 0;
    if(inputarray[1] == 0){
      ExpressionStateLocal = inputarray[0]-48;
    } else {
      ExpressionStateLocal = (10*(inputarray[0]-48)) + (inputarray[1]-48);
    }
    if(ExpressionStateLocal != ExpressionState){
      ExpressionState = ExpressionStateLocal;
      Effect = random(1, 6);
    }
  }
}

void colorSparkle(uint32_t color) {
  GearsStrip.setBrightness(Color_Brightness*2);
  int Pixel = random(GearsStrip.numPixels());
  GearsStrip.setPixelColor(Pixel, color);
  GearsStrip.show();
  GearsStrip.setPixelColor(Pixel, black);
}

void colorTwinkle(uint32_t color) {
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
    GetData();
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
 delay(3000);
}

void colorFade(uint32_t color){
    GearsStrip.setBrightness(Color_Brightness);
    for(int k = 0; k < Color_Brightness*2; k++) {
      int ExpressionStateLocal = ExpressionState;
      GetData();
      if(ExpressionState != ExpressionStateLocal){
        break;
      }
      GearsStrip.fill(color, 0, GearsStrip.numPixels());
      GearsStrip.setBrightness(k);
      GearsStrip.show();
      delay(25);
      Serial.println(k);
    }
    for(int k = Color_Brightness*2; k > 0; k--) {
      int ExpressionStateLocal = ExpressionState;
      GetData();
      if(ExpressionState != ExpressionStateLocal){
        break;
      }
      GearsStrip.fill(color, 0, GearsStrip.numPixels());
      GearsStrip.setBrightness(k);
      GearsStrip.show();
      delay(25);
      Serial.println(k);
    }
}

void colorWipe(uint32_t color) {
  GearsStrip.setBrightness(Color_Brightness);
  for(uint16_t i=0; i<GearsStrip.numPixels(); i++) {
    int ExpressionStateLocal = ExpressionState;
    GetData();
    if(ExpressionState != ExpressionStateLocal){
      break;
    }
    GearsStrip.setPixelColor(i, color);
    GearsStrip.show();
    delay(100);
  }
  for(uint16_t i=0; i<GearsStrip.numPixels(); i++) {
    int ExpressionStateLocal = ExpressionState;
    GetData();
    if(ExpressionState != ExpressionStateLocal){
      break;
    }
    GearsStrip.setPixelColor(i, black);
    GearsStrip.show();
    delay(100);
  }
}


void colorTheaterChase(uint32_t color) {
  GearsStrip.setBrightness(Color_Brightness);
  for(int a=0; a<10; a++) {
    for(int b=0; b<3; b++) {
      GearsStrip.clear();
      for(int c=b; c<GearsStrip.numPixels(); c += 3) {
        GearsStrip.setPixelColor(c, color);
      }
      int ExpressionStateLocal = ExpressionState;
      GetData();
      if(ExpressionState != ExpressionStateLocal){
        break;
      }
      GearsStrip.show();
      delay(200);
    }
  }
}

void Rainbow(int wait) {
  GearsStrip.setBrightness(Color_Brightness);
  for(long firstPixelHue = 0; firstPixelHue < 5*65536; firstPixelHue += 256) {
    for(int i=0; i<GearsStrip.numPixels(); i++) {
      int pixelHue = firstPixelHue + (i * 65536L / GearsStrip.numPixels());
      GearsStrip.setPixelColor(i, GearsStrip.gamma32(GearsStrip.ColorHSV(pixelHue)));
    }
    int ExpressionStateLocal = ExpressionState;
    GetData();
    if(ExpressionState != ExpressionStateLocal){
      break;
    }
    GearsStrip.show();
    delay(wait);
  }
}

void setup() {
  Serial.begin(9600);
  GearsStrip.begin();
  GearsStrip.show();
}

void loop() {
  GetData();
  switch(ExpressionState){
    case 0:
      GearsStrip.setBrightness(Color_Brightness/3);
      GearsStrip.fill(white, 0, GearsStrip.numPixels());
      GearsStrip.show();
      break;
    case 1:
      switch(Effect){
        case 1:
          colorSparkle(red);
          break;
        case 2:
          colorTwinkle(red);
          break;
        case 3:
          colorStrobe(red);
          break;
        case 4:
          colorFade(red);
          break;
        case 5:
          colorWipe(red);
          break;
        case 6:
          colorTheaterChase(red);
          break;
      }
      break;
    case 2:
      GearsStrip.clear();
      GearsStrip.show();
      break;
    case 3:
      switch(Effect){
        case 1:
          colorSparkle(yellow);
          break;
        case 2:
          colorTwinkle(yellow);
          break;
        case 3:
          colorStrobe(yellow);
          break;
        case 4:
          colorFade(yellow);
          break;
        case 5:
          colorWipe(yellow);
          break;
        case 6:
          colorTheaterChase(yellow);
          break;
      }
      break;
    case 4:
      switch(Effect){
        case 1:
          colorSparkle(pink);
          break;
        case 2:
          colorTwinkle(pink);
          break;
        case 3:
          colorStrobe(pink);
          break;
        case 4:
          colorFade(pink);
          break;
        case 5:
          colorWipe(pink);
          break;
        case 6:
          colorTheaterChase(pink);
          break;
      }
      break;
    case 5:
      switch(Effect){
        case 1:
          colorSparkle(light_blue);
          break;
        case 2:
          colorTwinkle(light_blue);
          break;
        case 3:
          colorStrobe(light_blue);
          break;
        case 4:
          colorFade(light_blue);
          break;
        case 5:
          colorWipe(light_blue);
          break;
        case 6:
          colorTheaterChase(light_blue);
          break;
      }
      break;
    case 6:
      switch(Effect){
        case 1:
          colorSparkle(deep_blue);
          break;
        case 2:
          colorTwinkle(deep_blue);
          break;
        case 3:
          colorStrobe(deep_blue);
          break;
        case 4:
          colorFade(deep_blue);
          break;
        case 5:
          colorWipe(deep_blue);
          break;
        case 6:
          colorTheaterChase(deep_blue);
          break;
      }
      break;
    case 7:
      switch(Effect){
        case 1:
          colorSparkle(orange);
          break;
        case 2:
          colorTwinkle(orange);
          break;
        case 3:
          colorStrobe(orange);
          break;
        case 4:
          colorFade(orange);
          break;
        case 5:
          colorWipe(orange);
          break;
        case 6:
          colorTheaterChase(orange);
          break;
      }
      break;
    case 8:
      switch(Effect){
        case 1:
          colorSparkle(green);
          break;
        case 2:
          colorTwinkle(green);
          break;
        case 3:
          colorStrobe(green);
          break;
        case 4:
          colorFade(green);
          break;
        case 5:
          colorWipe(green);
          break;
        case 6:
          colorTheaterChase(green);
          break;
      }
      break;
    case 9:
      switch(Effect){
        case 1:
          colorSparkle(red);
          break;
        case 2:
          colorTwinkle(red);
          break;
        case 3:
          colorStrobe(red);
          break;
        case 4:
          colorFade(red);
          break;
        case 5:
          colorWipe(red);
          break;
        case 6:
          colorTheaterChase(red);
          break;
      }
      break;
    case 10:
      Rainbow(10);
      break;
  }
  Serial.println(ExpressionState);
}
