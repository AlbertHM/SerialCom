//Basic

#include <Wire.h>

void setup()
{
  Wire.begin(); // join i2c bus (address optional for master)
}

void loop()
{
  
  Wire.beginTransmission(4); // transmit to device #4
  Wire.write(1);              // sends one byte  
  Wire.endTransmission();    // stop transmitting

  delay(500);
}
