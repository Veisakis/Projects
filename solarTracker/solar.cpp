#include <math.h>

#define PI 3.14159
#define DEGREES(x) x*PI/180.0
 
float beta(unsigned short  N){
	return (N-81) * (360.0/365.0);
}

float ET(float b){
	return 9.87*(sin(2*DEGREES(b))) - 7.53*(cos(DEGREES(b))) - 1.5*(sin(DEGREES(b)));
}

float suntime(float localtime, float Lloc, float ET){
	/* Subtract 60min from localtime,
	if day is between last Sunday of March,
	till last Sunday of October */
	return -4.0*(30.0-Lloc) + ET;
}

float delta(unsigned short N){
	return sin((360.0/365.0)*(284+N))*23.45;
}	

float omega(){
	return 0;
}
float theta(float d, float phi, float s, float omega){
	return 0;	
}
