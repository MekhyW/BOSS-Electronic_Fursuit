#include <Adafruit_NeoPixel.h>
#define LED_PIN 10
#define LED_COUNT 240
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
int Effect = 1;
uint32_t* activeColor = &white;
int receivedValue = 0;
int receivedValue_prev = 0;

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
  for (int i=0; i<(GearsStrip.numPixels())/5; i++) {
     GearsStrip.setPixelColor(random(GearsStrip.numPixels()), color);
     GearsStrip.show();
     delay(10);
   }
}

void colorStrobe(uint32_t color){
  GearsStrip.setBrightness(Color_Brightness/2);
  for(int j = 0; j < 5; j++) {
    GearsStrip.fill(color, 0, GearsStrip.numPixels());
    GearsStrip.show();
    delay(50);
    GearsStrip.fill(black, 0, GearsStrip.numPixels());
    GearsStrip.show();
    delay(50);
  }
 delay(1000);
}

void colorFade(uint32_t color){
    GearsStrip.setBrightness(Color_Brightness);
    for(int k = 0; k < Color_Brightness*2; k++) {
      GearsStrip.fill(color, 0, GearsStrip.numPixels());
      GearsStrip.setBrightness(k);
      GearsStrip.show();
      delay(10);
    }
    for(int k = Color_Brightness*2; k > 0; k--) {
      GearsStrip.fill(color, 0, GearsStrip.numPixels());
      GearsStrip.setBrightness(k);
      GearsStrip.show();
      delay(10);
    }
}

void colorWipe(uint32_t color) {
  GearsStrip.setBrightness(Color_Brightness);
  if (GearsStrip.getPixelColor(0) == 0)
  {
    for(uint16_t i=0; i<GearsStrip.numPixels(); i++) {
      GearsStrip.setPixelColor(i, color);
      GearsStrip.show();
      delay(10);
    }
  } else {
    for(uint16_t i=0; i<GearsStrip.numPixels(); i++) {
      GearsStrip.setPixelColor(i, black);
      GearsStrip.show();
      delay(10);
    }
  }
}


void colorTheaterChase(uint32_t color) {
  GearsStrip.setBrightness(Color_Brightness*2);
  for(int b=0; b<3; b++) {
    GearsStrip.clear();
    for(int c=b; c<GearsStrip.numPixels(); c += 3) {
      GearsStrip.setPixelColor(c, color);
    }
    GearsStrip.show();
    delay(200);
  }
}

void Rainbow(int wait) {
  GearsStrip.setBrightness(Color_Brightness*2);
  for(long firstPixelHue = 0; firstPixelHue < 65536; firstPixelHue += 512) {
    for(int i=0; i<GearsStrip.numPixels(); i++) {
      int pixelHue = firstPixelHue + (i * 65536L / GearsStrip.numPixels());
      GearsStrip.setPixelColor(i, GearsStrip.gamma32(GearsStrip.ColorHSV(pixelHue)));
    }
    GearsStrip.show();
    delay(wait);
  }
}

void Off() {
  GearsStrip.fill(black, 0, GearsStrip.numPixels());
  GearsStrip.show();
}

void readSerialPort() {
  if (Serial.available()) {
    receivedValue_prev = receivedValue;
    receivedValue = Serial.parseInt();
    Serial.flush();
  }
  while (Serial.available()){
    Serial.read();
  }
}

void setup() {
  Serial.begin(9600);
  GearsStrip.begin();
  GearsStrip.show();
  GearsStrip.setBrightness(Color_Brightness);
  colorStatic(white);
}

void loop() {
  readSerialPort();
  Serial.println(*activeColor);
  if (receivedValue != receivedValue_prev) {
    Effect = random(0, 8);
    receivedValue_prev = receivedValue;
    GearsStrip.fill(black, 0, GearsStrip.numPixels());
    GearsStrip.setBrightness(Color_Brightness);
  }
  switch (receivedValue) {
    case 99:
      Off();
      break;
    case 10:
      //Assistant listening
      break;
    case 11:
      //Assistant processing
      break;
    case 12:
      //Assistant responding
      break;
    case 13:
      //Message received
      break;
    case 14:
      //Processing media
      break;
    case 0:
      //neutral
      colorStatic(white);
      break;
    case 7:
      //Hypnotic
      Rainbow(10);
      break;
    default:
      switch (receivedValue) {
        case 1:
          //Angry
          activeColor = &red;
          break;
        case 2:
          //Disgusted
          activeColor = &green;
          break;
        case 3:
          //Sad
          activeColor = &deep_blue;
          break;
        case 4:
          //Happy
          activeColor = &yellow;
          break;
        case 5:
          //Scared
          activeColor = &purple;
          break;
        case 6:
          //Heart
          activeColor = &red;
          break;
        case 8:
          //Sexy
          activeColor = &pink;
          break;
        case 9:
          //Demonic
          activeColor = &black;
          break;
      }
      switch(Effect) {
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
      break;
  }
  delay(10);
}
