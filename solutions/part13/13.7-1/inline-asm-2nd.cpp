// Normal multiplication

#include <iostream>

void mult_array(int * array0, int lengArray, int multiplier0)
{
	__asm
	{
		mov esi, array0
		mov ecx, lengArray
		mov ebx, multiplier0
		L1:
		mov eax, [esi]
		mul ebx
		mov [esi], eax
		add esi, 4; DON T USE "TYPE DWORD", OTHERWISE PROGRAM HAS A BUG!
		loop L1
	}
}

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
