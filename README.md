
main source code of program in file assembler.py


execute command on terminal 

$ python assembler.py

it will genrate 4 files named
 symbol_table , litral_table , op.mylst , pass_01 
 op.mylst is opcode file , pass_01 is one pass of code other two are for symbols and litrals

in program line no 16 have flags discription every flag have a two value tuple (a,b) a discribs bit position in flag register and b discribs that it is set or unset


There are 3 other file 

opcode.json - it have all description about opcode table in form of dictonary of list of dictonary
test.asm - it is input to assembler
t1.lst - lst file genrated by nasm


thanks
