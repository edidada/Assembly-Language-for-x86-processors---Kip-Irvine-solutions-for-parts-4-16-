//This program uses void function which multiplies all array elements by a multilplier
// and saves multiplies elements in source array

#include <iostream>

void mult_array(int * array0, int lengArray, int multiplier0)
{
	for (int i = 0; i < lengArray; i++)
	{
		array0[i] = multiplier0*array0[i];
	}
}

int main()
{
	const int Z = 8;
	using namespace std;
	int array2[Z] = { 1,2,3, 0, 9 };
	int multiplier = 3;
	mult_array(array2, Z, multiplier);
	for (int j = 0; j < Z; j++)
		cout << array2[j] << "\t";
	return 0;
}
