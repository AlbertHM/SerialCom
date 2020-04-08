//Py-Mst-Slv 2

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
byte buffer1[7], buffer2[7];
unsigned int x, temp, data[7];

unsigned int sudutT0(unsigned int p)
{
  unsigned int u = 3600+((405*p)/180);
  return u;
}

void setup() {
  Wire.begin();
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(50);

  for (uint8_t pin=0; pin<16; pin++) 
  {
  pwm.setPWM(pin, sudutT0(90),4095);
  }
  pwm.setPWM(3, sudutT0(90), 4095);
  pwm.setPWM(7, sudutT0(50), 4095);
}

void loop() {
    if(Serial.available() >= 15){
      if(Serial.read() == 0xF5)
      {
        for(uint8_t i = 0;i<7;i++)
        {
          //Reading byte
          buffer1[i]=Serial.read();
          buffer2[i]=Serial.read();
          
          //Conversion to number
          data[i] = ((unsigned int)buffer1[i]<<8)+buffer2[i];
        }
        //Joint 1
        x = sudutT0(data[0]);
        pwm.setPWM(0,x,4095);
        
        // Joint 2 Servo kiri dan kanan
        x = sudutT0(data[1]);
        pwm.setPWM(1,x,4095);
        x = sudutT0(180-data[1]); //180 - theta
        pwm.setPWM(2,x,4095);
        
        //Joint 3 - 6, Gripper
        for(uint8_t u = 3; u<8; u++)
        {
          x = sudutT0(data[u-1]);
          pwm.setPWM(u,x,4095);
        }
        //delay(100);
      }
    }
}
