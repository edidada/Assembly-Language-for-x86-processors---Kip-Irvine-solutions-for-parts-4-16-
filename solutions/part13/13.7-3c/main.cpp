// 13.7 - 3 - Summing Three Arrays

#include <iostream>

extern "C" void Summing_Three_Arrays(int * array1, int * array2, int * array3, int array_length);

int main()
{
	using namespace std;
	const int array_length = 4;
	int array1[array_length] = { 0,1,2,3 };
	int array2[array_length] = { 1,2,3,4 };
	int array3[array_length] = { 2,3,4,5 };

	Summing_Three_Arrays(array1, array2, array3, array_length);

	for (int i = 0; i < array_length; i++)
		printf("%d ", array1[i]);

	return 0;
}
