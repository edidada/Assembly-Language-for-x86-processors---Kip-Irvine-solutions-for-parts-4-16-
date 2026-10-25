.586
.MODEL flat, C

mult_array proto,
array0: ptr dword,
lengArray: dword,
multiplier0: dword

.code

mult_array proc,
array0: ptr dword,
lengArray: dword,
multiplier0: dword

mov esi, array0
mov ecx, lengArray
mov ebx, multiplier0
L1 :
mov eax, [esi]
mul ebx
mov[esi], eax
add esi, 4; DON T USE "TYPE DWORD", OTHERWISE PROGRAM HAS A BUG!
loop L1

ret
mult_array endp
end
