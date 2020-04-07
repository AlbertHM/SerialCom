//Master-Slave-Series of Data

#include <Wire.h>
unsigned int send[7] = {252,253,254,255,256,257,258};
byte buffer1[7], buffer2[7];

void setup()
{
  Wire.begin(); // join i2c bus (address optional for master)
}

void loop()
{
  
  Wire.beginTransmission(4); // transmit to device #4
  for(int i = 0;i<7;i++)
  {
    buffer1[i]=send[i]>>8;
    buffer2[i]=send[i];
  }
  Wire.write(buffer1,7);
  Wire.write(buffer2,7);
  Wire.endTransmission();    // stop transmitting
  delay(500);
}
