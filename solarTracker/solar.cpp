#include <math.h>

#define PI 3.14159
#define DEGREES(x) x * 180.0/PI
#define RADIANS(x) x * PI/180.0
#define SIGN(x) (x > 0 ? 1 : -1)
 
float l_loc = 23.75;
unsigned short phi = 30;
 
unsigned short toMinutes(float clocktime){
	float hours, minutes;
	hours = floor(clocktime);
	minutes = clocktime - hours;
	return hours*60 + minutes*100;
}

float toHours(float percent_time){
	float hours, minutes;
	hours = floor(percent_time);
	minutes = 0.6 * (percent_time - hours);
	return hours + minutes;
}

float toClocktime(unsigned short mnt){
	unsigned short hours;
	float minutes;
	hours = mnt / 60;
	minutes = mnt % 60;
	return hours + minutes*0.01;
}

short minFromSolarMidday(float ts){
	return toMinutes(ts) - toMinutes(12.00);
}

float beta(unsigned short d){
	return (d-81) * (360.0/365.0);
}

float eqntime(float b){
	return 9.87*(sin(2*RADIANS(b))) - 7.53*(cos(RADIANS(b))) - 1.5*(sin(RADIANS(b)));
}

float suntime(float et, float tl){
	/* Subtract 60min from tl,
	if day is between last Sunday of March,
	till last Sunday of October */
	float ts_tl;
	ts_tl = -4.0*(30.0-l_loc) + et;	
	return toClocktime(toMinutes(tl) + ts_tl);
}

float delta(unsigned short d){
	return sin(RADIANS((360.0/365.0)*(284+d)))*23.45;
}	

float omegaS(float delta){
	return DEGREES(acos(-tan(RADIANS(phi))*tan(RADIANS(delta))));
}

float dayDuration(float ws){
	return ws * 2.0/15.0;
}

float sunrise(float n){
	return 12 - n/2;
}

float sunset(float n){
	return 12 + n/2;
}

float omega(float ts){
	return 0.25 * minFromSolarMidday(ts);
}

float thetazeta(float d, float w){
	return DEGREES(acos(sin(RADIANS(phi))*sin(RADIANS(d)) + cos(RADIANS(phi))*cos(RADIANS(d))*cos(RADIANS(w))));	
}

float sunheight(float uz){
	return 90 - uz;
}

float azimuth(float uz, float d, float w){
	return SIGN(w) * fabs(DEGREES(acos((cos(RADIANS(uz))*sin(RADIANS(phi))-sin(RADIANS(d)))/(sin(RADIANS(uz))*cos(RADIANS(phi))))));
} 

float servoAngle(unsigned short n, float tl){
	float d, et, ts, w, uz;

	d = delta(n);
	et = eqntime(beta(d));

	ts = suntime(et, tl);
	w = omega(ts);

	uz = thetazeta(d, w);
	return azimuth(uz, d, w);
}
