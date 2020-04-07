//2 bytes of data

#include <Wire.h>
unsigned int send = 252;
byte buffer1, buffer2;

void setup()
{
  Wire.begin(); // join i2c bus (address optional for master)
}

void loop()
{
  
  Wire.beginTransmission(4); // transmit to device #4
  buffer1 = send >> 8; //high order byte contoh kasus 258, ini dec(1) ; 256*1 + 2 = 258
  buffer2 = send;      //lower order byte contoh kasus 256 ini dec(2)
  Wire.write(buffer1);              // sends one byte
  Wire.write(buffer2);  
  Wire.endTransmission();    // stop transmitting
  if(send==258)
  {
    send=252;
  }
  else
  {
    send++;
  }
  delay(500);
}
