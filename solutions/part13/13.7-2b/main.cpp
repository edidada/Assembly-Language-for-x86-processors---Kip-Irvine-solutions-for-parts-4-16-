#include <iostream>

extern "C" int Longest_Increasing_Sequence(int * array1, int length_array, int * increase_sequence);

int main()
{
	using namespace std;
	const int length_array = 10;
	int array1 [length_array] = { -5, 10, 20, 14, 17, 26, 42, 22, 19, -5 };
	cout << "Array is: ";
	for (int i = 0; i < length_array; i++)
		printf("%d ", array1[i]);
	cout << endl;
	int increase_sequence [length_array] = {0};
	int counter = Longest_Increasing_Sequence(array1, length_array, increase_sequence);
	cout << "Length of the longest increasing sequence is ";
	printf("%d\n", counter);
	cout << "Sequence is: ";
	for (int i = 0; i < counter; i++)
		cout << increase_sequence[i] << " ";
	cout << endl;
	return 0;
}
