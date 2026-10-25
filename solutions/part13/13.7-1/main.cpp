// Linking ASM code to C++

#include <iostream>

extern "C" void mult_array(int * array0, int lengArray, int multiplier0);

int main()
{
	const int Z = 8;
	using namespace std;
	int array2[Z] = { 21,2,3,4 };
	int multiplier = 8;
	mult_array(array2, Z, multiplier);
	for (int j = 0; j < Z; j++)
		cout << array2[j] << "\n";
	return 0;
}
