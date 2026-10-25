;13.7 - 3 - Summing Three Arrays

.586
.MODEL flat, C

Summing_Three_Arrays proto,
array1 : ptr dword,
array2: ptr dword,
array3: ptr dword,
array_length : dword

.code

Summing_Three_Arrays proc,
array1 : ptr dword,
array2: ptr dword,
array3: ptr dword,
array_length : dword

mov esi, array1
mov edi, array2
mov edx, array3
mov ecx, array_length
L1 :
mov eax, [edi]
add eax, [edx]
add[esi], eax
add esi, 4
add edi, 4
add edx, 4
loop L1

ret
Summing_Three_Arrays endp
end
