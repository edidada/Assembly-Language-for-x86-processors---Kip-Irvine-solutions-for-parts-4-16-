// Here multiplication is substituted by a simple addition

#include <iostream>

void mult_array(int * array0, int lengArray, int multiplier0)
{
	__asm
	{
		mov esi, array0
		mov ecx, lengArray
		L1:
		push ecx
		mov eax, [esi]
		mov ebx, [esi]
		mov ecx, multiplier0
		dec ecx
		L2:
		add eax, ebx
		loop L2
		mov [esi], eax
		add esi, 4; DON T USE "TYPE DWORD", OTHERWISE PROGRAM HAS A BUG!
		pop ecx
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
