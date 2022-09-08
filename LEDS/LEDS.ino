#include <Adafruit_NeoPixel.h>
#include <ros.h>
#include <std_msgs/Int8MultiArray.h>
#define LED_PIN 39
#define LED_COUNT 64
Adafruit_NeoPixel GearsStrip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
int Color_Brightness = 25;
int8[LED_COUNT] Red;
int8[LED_COUNT] Green;
int8[LED_COUNT] Blue;

void redCallback(const std_msgs::Int8MultiArray& msg)
{
  Red = msg.data;
}
void greenCallback(const std_msgs::Int8MultiArray& msg)
{
  Green = msg.data;
}
void blueCallback(const std_msgs::Int8MultiArray& msg)
{
  Blue = msg.data;
}

ros::NodeHandle nodehandle;
ros::Subscriber<std_msgs::UInt16> sub_red("led_red", &redCallback);
ros::Subscriber<std_msgs::UInt16> sub_green("led_green", &greenCallback);
ros::Subscriber<std_msgs::UInt16> sub_blue("led_blue", &blueCallback);

void setup() {
  nodehandle.getHardware()->setBaud(115200);
  nodehandle.initNode();
  nodehandle.subscribe(sub_red);
  nodehandle.subscribe(sub_green);
  nodehandle.subscribe(sub_blue);
  GearsStrip.begin();
  GearsStrip.show();
  GearsStrip.setBrightness(Color_Brightness);
}

void loop() {
  for (int i = 0; i < sqrt(LED_COUNT)) {
    for (int j = 0; j < sqrt(LED_COUNT)) {
      uint32_t color = GearsStrip.Color(Red[i][j], Green[i][j], Blue[i][j]);
      GearsStrip.setPixelColor(i*sqrt(LED_COUNT)+j, color);
    }
  }
  nodehandle.spinOnce();
}
