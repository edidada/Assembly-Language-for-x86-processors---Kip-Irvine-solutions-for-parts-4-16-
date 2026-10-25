// ASM subroutine returns length of the longest increasing sequence.

#include <iostream>

extern "C" int Longest_Increasing_Sequence(int * array1, int length_array);

int main()
{
	using namespace std;
	const int length_array = 10;
	int array1 [length_array] = { 1,2,3,1,2,3,4};
	int increase_sequence [length_array] = {0};
	int counter = Longest_Increasing_Sequence(array1, length_array);
	printf("%d\n", counter);
	return 0;
}
