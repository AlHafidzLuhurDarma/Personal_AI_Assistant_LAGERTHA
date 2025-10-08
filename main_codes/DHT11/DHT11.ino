#include <DHT.h>
#define Type DHT11
int sensePin=12;
int waktu=500;
float humidity;
float tempC;
float tempF;


DHT DH(sensePin,Type);

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
DH.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
humidity=DH.readHumidity();
tempC=DH.readTemperature();
tempF=DH.readTemperature(true);

  while(Serial.available()==0){
    }
  String cmd = Serial.readStringUntil('\a');
  if (cmd == "humidity"){
humidity_sensor();
  }
}

void humidity_sensor(){
  Serial.print("The Humidity is ");
Serial.print(humidity);
Serial.print(" percent");
Serial.print(" and the Temperature is ");
Serial.print(tempC);
Serial.print(" degree celcius ");
Serial.print("or ");
Serial.print(tempF);
Serial.println(" degree fahrenheit");
delay(waktu);
  }
