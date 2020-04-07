/*
SUCCCEEESSSSS!!!!
*/

#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>
#include <Wire.h>
#define OLED_ADDR 0x3c

Adafruit_SSD1306 display(-1);

int a,b,numb;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN,OUTPUT);
  display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
  display.clearDisplay();
  display.display();
  
  display.drawPixel(0, 0, WHITE);
  display.drawPixel(127, 0, WHITE);
  display.drawPixel(0, 63, WHITE);
  display.drawPixel(127, 63, WHITE);

  // display a line of text
  display.setTextSize(1); //INI PERLU
  display.setTextColor(WHITE); //INI PERLU
  display.setCursor(20,30);
  display.println("Bekerja");
  display.print("New line");

  // update display with all of the above graphics
  display.display();
}

void loop() {
  // Serial.read() membaca tiap byte
  if(Serial.available()>1)
  {
    b = Serial.read(); //lower order byte dikirimkan terlebih dahulu
    a = Serial.read();
    numb = (a<<8) | b;
  display.clearDisplay();
  display.setCursor(0,0);
    display.println(b); //lower order byte
    display.println(a); //high order byte
    display.println(numb);
    display.display();
    if(numb==1)
    {
    digitalWrite(LED_BUILTIN,HIGH);
    delay(100);
    digitalWrite(LED_BUILTIN,LOW);
    delay(100);      
    }
  }

}
