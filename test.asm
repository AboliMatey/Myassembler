section .data
	c dd 1
	b dd 1255
	msg db "addition is %d",10,0
	h db "22"
	e dd 12
	d dd 5
	a dd 2
	q dd 34

	
section .bss
	sum resd 3
	aa resd 1
	cc resb 1
	bb resd 1

section .text
	global main
	extern printf

main:	
  mov eax,dword[c]
	mov ebx,dword[b]
	mov al,bl
	mov ch,bh
	mov ax,bx
	mov ecx,edx
	mov eax,2332
	mov ax,2132
	mov al,12
  mov ah,23
	mov ebx,dword[c]
	mov eax,dword[b]
	mov ax,word[e]
	mov bx,word[e]
	mov cx,word[c]
	mov ah,byte[e]
	mov bh,byte[b]
	mov ch,byte[d]
	mov di,word[b]
	mov dword[c],ecx
	mov dword[c],eax
	mov word[b],ax
	mov dword[b],edx
	mov word[b],dx
	mov byte[c],al
	mov dword[b],456
	mov word[b],124
	mov byte[e],78
abc:

	add eax,ebx
	add ecx,edx
	add ebx,esi
	add esp,edx
	add ax,bx
	add cx,sp
	add bp,di
	add al,dl
	add ah,ch
	add bh,cl
	add eax,dword[c]
	add esi,dword[b]
	add ax,word[b]
	add sp,word[c]
	add al,byte[c]
	add cl,byte[e]
	add dword[c],edx
	add word[b],di
	add dword[e],eax
	add word[c],ax
	add byte[a],al
	add eax,32
	add ecx,69
	add ax,13
	add cx,34
	add si,31
	add al,4
	add dl,3
	add bl,67
	add ah,45
	add dh,55

	sub eax,ebx
	sub ecx,edx
	sub ebx,esi
	sub esp,edx
	sub ax,bx
	sub cx,sp
	sub bp,di
	sub al,dl
	sub ah,ch
	sub bh,cl
	sub eax,dword[c]
	sub esi,dword[b]
	sub ax,word[b]
	sub sp,word[c]
	sub al,byte[c]
	sub cl,byte[e]
	sub dword[c],edx
	sub word[b],di
	sub dword[e],eax
	sub word[c],ax
	sub byte[a],al
	sub eax,32
	sub ecx,69
	sub ax,13
	sub cx,34
	sub si,31
	sub dl,3
	sub bl,67
	sub ah,45
	sub dh,55
pqr:
	mul ecx
	mul edx
	mul esi
	mul eax
	mul ax
	mul sp
	mul si
	mul al
	mul cl
	mul ah

	div ecx
	div edx
	div eax
	div ax
	div sp
	div si
	div al
	div cl
	div ah
  cld
  std
  cld
  std
	push eax
	push ecx
	push edx
	push edi
	push ax
	push sp
	push si
	
	add esp,8
	rep movsb
  rep lodsb
  repe scasb
  scasb
  movsb


