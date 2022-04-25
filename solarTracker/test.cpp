#include <stdio.h>
#include "solar.h"

int main(){
	printf("B: %f\tET: %f\n", beta(60), ET(beta(60))); 
	printf("Suntime Difference: %f\n", suntime(12.0, 23.75, ET(beta(60))));
}
