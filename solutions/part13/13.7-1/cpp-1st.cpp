// This program multiplies elements of one array and places multiplied elements to another array.
#include <iostream>

int main()
{
	const int Z = 3;
	using namespace std;
	int array2[Z] = { 1,2,3 };
	int array3[Z];
	int multiplier = 3;
	for (int i = 0; i<Z;i++)
	{
		array3[i] = array2[i] * multiplier;
	}
	for (int j = 0; j < Z; j++)
		cout << array3[j] << "\t";
	return 0;
}
