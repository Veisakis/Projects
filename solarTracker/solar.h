#ifndef SOLAR
#define SOLAR

unsigned short toMinutes(float clocktime);
float toHours(float percent_time);
float toClocktime(unsigned short mnt);
short minFromSolarMidday(float ts);
float beta(unsigned short d);
float eqntime(float b);
float suntime(float tl, float et);
float delta(unsigned short d);
float omegaS(float delta);
float dayDuration(float ws);
float sunrise(float n);
float sunset(float n);
float omega(float ts);
float thetazeta(float d, float w);
float azimuth(float uz, float d, float w);
float servoAngle(unsigned short n, float tl);

#endif
