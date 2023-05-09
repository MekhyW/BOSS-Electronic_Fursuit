#include <Adafruit_NeoPixel.h>
#define LED_PIN 10
#define LED_COUNT 120
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
      GearsStrip.fill(color, 0, GearsStrip.numPixels());
      GearsStrip.setBrightness(k);
      GearsStrip.show();
      delay(25);
    }
    for(int k = Color_Brightness*2; k > 0; k--) {
      GearsStrip.fill(color, 0, GearsStrip.numPixels());
      GearsStrip.setBrightness(k);
      GearsStrip.show();
      delay(25);
    }
}

void colorWipe(uint32_t color) {
  GearsStrip.setBrightness(Color_Brightness);
  for(uint16_t i=0; i<GearsStrip.numPixels(); i++) {
    GearsStrip.setPixelColor(i, color);
    GearsStrip.show();
    delay(100);
  }
  for(uint16_t i=0; i<GearsStrip.numPixels(); i++) {
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
  }
  if (receivedValue == 99) {
    activeColor = &black;
    Off();
  }
  else {
    if (receivedValue == 0) {
      colorStatic(white);
    }
    else if (receivedValue == 7) {
      Rainbow(10);
    }
    else {
      switch (receivedValue) {
        case 1:
        case 8:
          activeColor = &red;
          break;
        case 2:
          activeColor = &green;
          break;
        case 3:
          activeColor = &deep_blue;
          break;
        case 4:
          activeColor = &yellow;
          break;
        case 5:
          activeColor = &purple;
          break;
        case 6:
          activeColor = &pink;
          break;
        default:
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
    }
  }
  delay(10);
}
