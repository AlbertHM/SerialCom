//Basic

#include <Wire.h>

void setup()
{
  Wire.begin(4); //Slave address = 4
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
    Serial.println(Wire.read());
}
