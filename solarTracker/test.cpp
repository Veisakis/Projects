#include <stdio.h>
#include "solar.h"

int main(){
	float d, w, ws, N, n, phi;
	
	n = 44;
	phi = 43;

	d = delta(n);
	w = omega(9.30);

	printf("Delta: %.2f\n", d);
	printf("Omega: %.2f\n", w);
	printf("Gamms: %.2f\n", azimuth(thetazeta(d, phi, w), phi, d, w));
}
