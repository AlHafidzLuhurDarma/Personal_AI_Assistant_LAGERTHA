#include <FastLED.h>
#include <Adafruit_Fingerprint.h>

// Desk_1 (long)
#define PIN_LED_1 4  //kabel kuning
#define NUM_LEDS_1 40

// Desk_2 (medium)
#define PIN_LED_2 7  //kabel hijau
#define NUM_LEDS_2 19

// Desk_3 (short)
#define PIN_LED_3 8  //kabel ungu
#define NUM_LEDS_3 19

CRGB leds_1[NUM_LEDS_1];
CRGB leds_2[NUM_LEDS_2];
CRGB leds_3[NUM_LEDS_3];


#if (defined(__AVR__) || defined(ESP8266)) && !defined(__AVR_ATmega2560__)
SoftwareSerial mySerial(2, 3); //(Pin 2 = oren, Pin 3 = putih)

#else

#define mySerial Serial1

#endif


Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

String finger_condition = "On"; 

void setup()
{
  Serial.begin(9600);
  while (!Serial);  // For Yun/Leo/Micro/Zero/...
  delay(100);
  Serial.println("\n\nAdafruit finger detect test");

  // set the data rate for the sensor serial port
  finger.begin(57600);
  delay(5);
  if (finger.verifyPassword()) {
    Serial.println("Found fingerprint sensor!");
  } else {
    Serial.println("Did not find fingerprint sensor :(");
    while (1) { delay(1); }
  }
  finger.getParameters();
  finger.getTemplateCount();

  if (finger.templateCount == 0) {
    Serial.print("Sensor doesn't contain any fingerprint data. Please run the 'enroll' example.");
  }
  else {
    Serial.println("Waiting for valid finger...");
  }
FastLED.addLeds<WS2812B, PIN_LED_1, RGB>(leds_1, NUM_LEDS_1);
FastLED.addLeds<WS2812B, PIN_LED_2, RGB>(leds_2, NUM_LEDS_2);
FastLED.addLeds<WS2812B, PIN_LED_3, RGB>(leds_3, NUM_LEDS_3);
FastLED.setBrightness(70);

}

void loop()                     // run over and over again
{
  if (finger_condition == "On"){
  getFingerprintID();
  red();            
}
  else{
    green();
    }
}

uint8_t getFingerprintID() {
  uint8_t p = finger.getImage();
  switch (p) {
    case FINGERPRINT_OK:
      break;
    case FINGERPRINT_NOFINGER:
      //Serial.println("No finger detected");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      return p;
    case FINGERPRINT_IMAGEFAIL:
      return p;
    default:
      return p;
  }

  // OK success!

  p = finger.image2Tz();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  // OK converted!
  p = finger.fingerSearch();
  if (p == FINGERPRINT_OK) {
    Serial.println("Found a print match!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_NOTFOUND) {
    Serial.println("Did not find a match");
    return p;
  } else {
    Serial.println("Unknown error");
    return p;
  }

  // found a match!
  Serial.print("Found ID #"); Serial.print(finger.fingerID);
  Serial.print(" with confidence of "); Serial.println(finger.confidence);
  finger_condition = "Off";
  return finger.fingerID;
}

// returns -1 if failed, otherwise returns ID #
int getFingerprintIDez() {
  uint8_t p = finger.getImage();
  if (p != FINGERPRINT_OK)  return -1;

  p = finger.image2Tz();
  if (p != FINGERPRINT_OK)  return -1;

  p = finger.fingerFastSearch();
  if (p != FINGERPRINT_OK)  return -1;

  // found a match!
  Serial.print("Found ID #"); Serial.print(finger.fingerID);
  Serial.print(" with confidence of "); Serial.println(finger.confidence);
  finger_condition = "Off";
  return finger.fingerID;
}

void red(){
    fill_solid(leds_1, NUM_LEDS_1, CRGB(0,255,0)); //Red
  fill_solid(leds_2, NUM_LEDS_2, CRGB(0,255,0));
  fill_solid(leds_3, NUM_LEDS_3, CRGB(0,255,0));
  FastLED.show();
  delay(50);
  }

void green(){
    fill_solid(leds_1, NUM_LEDS_1, CRGB(255,0,0)); //Green
  fill_solid(leds_2, NUM_LEDS_2, CRGB(255,0,0));
  fill_solid(leds_3, NUM_LEDS_3, CRGB(255,0,0));
  FastLED.show();
  delay(50);
  }
