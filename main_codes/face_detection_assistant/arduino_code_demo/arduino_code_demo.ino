#include <FastLED.h>

#define PIN_LED 7
#define NUM_LEDS 5
String myCmd;

CRGB leds[NUM_LEDS];
void setup() {
  // put your setup code here, to run once:
FastLED.addLeds<WS2812B, PIN_LED, RGB>(leds, NUM_LEDS);
FastLED.setBrightness(30);
Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available()==0){
    
    }
  myCmd = Serial.readStringUntil('\r');
  if (myCmd == "no_data"){
  fill_solid(leds, NUM_LEDS, CRGB(0,255,0));
  FastLED.show();
    }
  if (myCmd == "face"){
  fill_solid(leds, NUM_LEDS, CRGB(255,0,0));
  FastLED.show();
  }  
}

  
