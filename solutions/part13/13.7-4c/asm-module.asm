; 13.7 - 4 - Prime Number Program
; Calling C functions from ASM

.586
.MODEL flat, C

printf PROTO, pString : PTR BYTE, args : VARARG
scanf PROTO, pFormat : PTR BYTE, args : VARARG

.data

prime_numbers dword 2, 3, 5, 7, 11, 13, 17, 19, 23, 29
number dword 0

string byte "Please enter number: ",0
printf_string byte "%d", 0dh, 0ah, 0
scanf_string byte "%d", 0

.code
asmMain PROC

INVOKE printf, ADDR string
invoke scanf, addr scanf_string, addr number

mov esi, offset prime_numbers
mov ecx, lengthof prime_numbers
L1 :
mov eax, number
mov edx, 0
mov ebx, [esi]
div ebx
cmp edx, 0
je not_prime_number
add esi, 4
loop L1

prime_number :
mov eax, 1
INVOKE printf, ADDR printf_string, eax
jmp L2

not_prime_number :
mov eax, 0
INVOKE printf, ADDR printf_string, eax

L2 :

ret
asmMain ENDP
END
