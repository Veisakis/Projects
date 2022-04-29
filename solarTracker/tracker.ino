#include <Servo.h>
#include "solar.h"

Servo myservo;

unsigned short potpin_hour = A0;
unsigned short potpin_day = A1;

unsigned short day_val;
float hour_val;
float angle;

void setup() {
  myservo.attach(9);

  day_val = analogRead(potpin_day);
  day_val = map(day_val, 0, 1023, 1, 365);

  hour_val = analogRead(potpin_hour);
  hour_val = map(hour_val, 0, 1023, 0, 2459);
  hour_val *= 0.01;
}

void loop() {
  angle = servoAngle(day_val, hour_val);
  myservo.write(angle);

  delay(1000);
  hour_val += 0.01;
}
