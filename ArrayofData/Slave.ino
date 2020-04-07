//Master-Slave-Series of Data

#include <Wire.h>

byte temp1[7], temp2[7];
unsigned int data[7];

void setup()
{
  // put your setup code here, to run once:
  Wire.begin(4);
  Wire.onReceive(receiveEvent);
  Serial.begin(9600);
}

void loop()
{
  
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany)
{
  Serial.print("Length : ");
  Serial.print(howMany);
  Serial.print(" ");
  if(Wire.available() >= 14)
  {
    for(int i = 0;i<7;i++)
    {
      temp1[i]=Wire.read();
    }
    for(int i = 0;i<7;i++)
    {
      temp2[i]=Wire.read();
    }
    for(int i = 0;i<7;i++)
    {
      data[i] = ((unsigned int)temp1[i]<<8)+temp2[i];
      Serial.print(data[i]);
      Serial.print(" ");
    }
    Serial.println("");
    
  }
}
