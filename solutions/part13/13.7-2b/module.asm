.586
.MODEL flat, C

Longest_Increasing_Sequence proto,
array1: ptr dword,
length_array : dword,
increase_sequence : ptr dword

.code

Longest_Increasing_Sequence proc uses ebx ecx edx esi edi,
array1 : ptr dword,
length_array : dword,
increase_sequence : ptr dword
local counter: dword
local position: dword

		mov counter, 0
		mov esi, array1
		mov edi, array1
		add edi, 4
		mov ecx, length_array
		mov edx, 0; set counter
		L1 :
		mov eax, [esi]
		mov ebx, [edi]
		cmp ebx, eax
		jl L2
		inc edx; if (i + 1) > (i), then increase counter
		jmp L3
		L2 : ; here current counter in EDX compared to previously saved value in COUNTER
		mov eax, counter
		cmp edx, eax
		jb L3; if current value in EDX is bigger than that previously saved in COUNTER, then EDX is saved in counter
		mov counter, edx
		mov position, esi; save index of last member of the longest sequence
		mov edx, 0
		L3:
		add esi, 4
		add edi, 4
		loop L1

		mov esi, position
		mov eax, counter
		mov ebx, 4; type dword
		mul ebx
		sub esi, eax
		mov edi, increase_sequence
		mov ecx, counter
		inc ecx
		L4 :
		mov eax, [esi]
		mov[edi], eax
		add esi, 4
		add edi, 4
		loop L4

		mov eax, counter
		inc eax

ret
Longest_Increasing_Sequence endp
end
