#ifndef SOLAR
#define SOLAR

float beta(unsigned short N);
float ET(float b);
float suntime(float localtime, float Lloc, float ET);
float delta(unsigned short N);

#endif
