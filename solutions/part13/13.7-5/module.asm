; IndexOf function (IndexOf.asm)

.586
.model flat,C

IndexOf PROTO,
srchVal:DWORD, arrayPtr:PTR DWORD, count:DWORD

.code

IndexOf PROC USES ecx esi edi,
srchVal:DWORD, arrayPtr:PTR DWORD, count:DWORD

NOT_FOUND = -1

mov eax,srchVal
mov ecx,count
mov esi,arrayPtr
mov edi, ecx
sub edi, 4

L1:
cmp [esi+edi*4],eax
je found
dec edi
loop L1

notFound:
mov al,NOT_FOUND
jmp short exit

found:
mov eax,edi

exit:
ret
IndexOf ENDP
END
