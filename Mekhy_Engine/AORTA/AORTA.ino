#include <Adafruit_NeoPixel.h>
#define LED_PIN 39
#define LED_COUNT 42
Adafruit_NeoPixel GearsStrip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
int PixelHeight[42] = {25, 27, 29, 31, 33, 32, 30, 28, 26, 24, 22, 19, 17, 16, 18, 21, 23, 20, 15, 12, 9, 7, 7, 9, 12, 15, 20, 22, 23, 23, 22, 10, 13, 14, 11, 8, 5, 2, 4, 6};
int Color_Brightness = 50;
uint32_t white = GearsStrip.Color(255, 255, 255);
uint32_t red = GearsStrip.Color(255, 0, 0);
uint32_t yellow = GearsStrip.Color(255, 255, 0);
uint32_t pink = GearsStrip.Color(255, 0, 255);
uint32_t deep_blue = GearsStrip.Color(0, 0, 255);
uint32_t light_blue = GearsStrip.Color(0, 255, 255);
uint32_t orange = GearsStrip.Color(255, 128, 0);
uint32_t green = GearsStrip.Color(0, 255, 0);
int ExpressionState = 0;
int Volume = 0;
int SpectogramLevel = 0;
byte inputarray[10];

void Spectogram(uint32_t color){
  for(int i = 0; i < LED_COUNT; i++){
    if(SpectogramLevel > PixelHeight[i]){
      GearsStrip.setPixelColor(i, color);
    } else {
      GearsStrip.setPixelColor(i, 0, 0, 0);
    }
  }
}

void theaterChase(uint32_t color, int wait) {
  for(int a=0; a<10; a++) {
    for(int b=0; b<3; b++) {
      GearsStrip.clear();
      for(int c=b; c<GearsStrip.numPixels(); c += 3) {
        GearsStrip.setPixelColor(c, color);
      }
      GearsStrip.show();
      delay(wait);
    }
  }
}

void Rainbow(int wait) {
  for(long firstPixelHue = 0; firstPixelHue < 5*65536; firstPixelHue += 256) {
    for(int i=0; i<GearsStrip.numPixels(); i++) {
      int pixelHue = firstPixelHue + (i * 65536L / GearsStrip.numPixels());
      GearsStrip.setPixelColor(i, GearsStrip.gamma32(GearsStrip.ColorHSV(pixelHue)));
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
  SpectogramLevel = map(Volume, 0, 255, 0, 33);
  switch(ExpressionState){
    case 0:
      Spectogram(white);
      break;
    case 1:
      Spectogram(white);
      break;
    case 2:
      Spectogram(white);
      break;
    case 3:
      Spectogram(white);
      break;
    case 4:
      Spectogram(red);
      break;
    case 5:
      GearsStrip.clear();
      break;
    case 6:
      Spectogram(yellow);
      break;
    case 7:
      Spectogram(pink);
      break;
    case 8:
      Spectogram(light_blue);
      break;
    case 9:
      Spectogram(deep_blue);
      break;
    case 10:
      Spectogram(orange);
      break;
    case 11:
      Spectogram(green);
      break;
    case 12:
      theaterChase(red, 50);
      break;
    case 13:
      Rainbow(10);
      break;
  }
  GearsStrip.setBrightness(Color_Brightness);
  GearsStrip.show();
  Serial.print(ExpressionState);
  Serial.print("   ");
  Serial.println(Volume);
}
