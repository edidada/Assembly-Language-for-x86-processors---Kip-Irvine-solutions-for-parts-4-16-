//13.7 - 4 - Prime numbers

#include <iostream>

extern "C" int prime_numbers(int number);

int main()
{
	using namespace std;
	int number;
	cout << "Please enter a number: ";
	cin >> number;
	int x = prime_numbers(number);
	if (x == 1)
		printf("This is prime number.\n");
	else
		printf("This is not prime number.\n");
	return 0;
}
