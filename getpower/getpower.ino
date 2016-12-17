#include <Wire.h>
#include <Adafruit_INA219.h>

Adafruit_INA219 ina219;

void setup(void) 
{
  uint32_t currentFrequency;   
  Serial.begin(115200);
  ina219.begin();
}

void loop(void) 
{
  float current_mA = 0;
  current_mA = ina219.getCurrent_mA();
  
  //Power
  float power_W = current_mA * 19/1000;
  Serial.println(power_W);
  delay(20);
}
