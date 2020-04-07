//2 bytes of data

#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>
#include <Wire.h>
#define OLED_ADDR 0x3c

Adafruit_SSD1306 display(-1);

byte temp1, temp2;
int temp3;
unsigned int data;

void setup()
{
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
  Serial.print("Received data length : ");
  Serial.print(howMany); //jumlah byte dalam transport ini
  if(Wire.available() >= 2)
  {
    Serial.print(" | DATA : ");
    temp1 = Wire.read();
    temp2 = Wire.read();
    Serial.print(temp1);
    Serial.print(" ");
    Serial.print(temp2);
    Serial.print(" ");
    data = ((unsigned int)temp1<<8)+temp2;
    Serial.println(data);
  }
}
