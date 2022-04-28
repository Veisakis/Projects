#ifndef SOLAR
#define SOLAR

unsigned short toMinutes(float clocktime);
float toHours(float percent_time);
short minFromSolarMidday(float ts);
float beta(unsigned short d);
float eqntime(float b);
float suntime(float localtime, float lloc, float et);
float delta(unsigned short d);
float omegaS(float phi, float delta);
float dayDuration(float ws);
float sunrise(float n);
float sunset(float n);
float omega(float ts);
float thetazeta(float d, float phi, float w);
float azimuth(float uz, float phi, float d, float w);

#endif
