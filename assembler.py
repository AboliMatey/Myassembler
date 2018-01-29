import fileinput
import sys
import re
import json
from pprint import pprint

with open('opcode.json') as op_codes:
    ins_opcode = json.load(op_codes)

sym_dis = {"sym_n":"","type":"","status":"","value":"","size":0,"s_add":0}
sym_tab = []

lit_dis = {"lit_n":"","type":"","hex_value":""}
lit_tab = []

flags = {"cf":(0,0),"df":(10,0),"zf":(6,0),"of":(11,0),"sf":(7,0),"af":(4,0),"pf":(2,0)} #flags structure

r32 = ['eax','ecx','edx','ebx','esp','ebp','esi','edi']
r16 = ['ax','cx','dx','bx','sp','bp','si','di']
r8 = ['al','cl','dl','bl','ah','ch','dh','bh']
opr = ['r8','r16','r32','imm','dword','word','byte']
opcode = ['000','001','010','011','100','101','110','111']
mod = ['00','01','10','11']
op2 = ["mov","add","sub","mul","div","movs"]
op1 = ["push","jmp","lods","scas","rep","repe","repne"]
op0 = ["lodsb","lodsw","lodsd","movsb","movsw","movsd","scasb","scasw","scasd","std","cld"]

def sym_entry(a,b,c,d,e,f):
    sym_dis["sym_n"] = a
    sym_dis["type"] = b
    sym_dis["status"] = c
    sym_dis["value"] = d
    sym_dis["size"] = e
    sym_dis["s_add"] = f
    sym_tab.append(sym_dis.copy())

def litaral_entry(a,b,c):
    lit_dis["lit_n"] = a
    lit_dis["type"] = b
    lit_dis["hex_value"] = c
    lit_tab.append(lit_dis.copy())

def rev_big(val):
    l = [val[i:i+2] for i in range(0,len(val),2)]
    l = l[::-1]
    l = ''.join(l)
    return l
    
def address(val):
    val = format(int(val),'X')
    if(len(val)%2 != 0):
        val = ''.join(('0',val))
    return str(val).zfill(8)

def bss_assem(val):
    return str(val).zfill(8)

def big_endian(val):
        val = format(int(val),'X')
        if(len(val)%2 != 0):
                val = ''.join(('0',val))
        val = rev_big(val)
        k = 8 - len(val)
        for i in range(k):
                val = ''.join((val,'0'))
        return val
def index(x):
    y = str(x)
    l = 8-len(y)
    for i in range(l):
        y = ''.join((' ',y))
    return y

def cal_opr_opcode(x):
    x1 = x[0:4]
    x2 = x[4:]
    x1 = format(int(x1,2),'x').upper()
    x2 = format(int(x2,2),'x').upper()
    return x1+x2

def search_ins_opcode(ins,ls_opr):
    alpha_ins_ls = ins_opcode[ins[0]]
    for i in alpha_ins_ls:
        if i["operator"] == ins and i["operands"] == ls_opr :
            return i["opcode"]

def lookup_symbol_add(s_name):
    for i in sym_tab:
        if i['sym_n'] == s_name:
            return i['s_add']

def gen_opcode(ins,s):
    if (len(s) == 0):
        insop = search_ins_opcode(ins,[])
        return insop + "$ "

    if (len(s) == 1):
        if(s[0] in r32):
            ind = r32.index(s[0])
            insop = search_ins_opcode(ins,["r32"])
            return insop + str(ind) + "$#reg32_" + str(ind)
        if(s[0] in r16):
            ind = r16.index(s[0])
            insop = search_ins_opcode(ins,["r16"])
            return insop + str(ind) + "$#reg16_" + str(ind)
        if(s[0] in r8):
            ind = r8.index(s[0])
            insop = search_ins_opcode(ins,["r8"])
            return insop+ str(ind) + "$#reg8_" + str(ind)
        if('dword' in s[0]):
            insop = search_ins_opcode(ins,["m32"])
            return insop + "$#reg32_" + str(ind)
        if('word' in s[0]):
            insop = search_ins_opcode(ins,["m16"])
            return insop + "$#mem32"
        if('byte' in s[0]):
            insop = search_ins_opcode(ins,["m8"])
            return insop + "$#mem16"
        if(s[0].isdigit() == True):
            insop = search_ins_opcode(ins,["imm8"])
            x = format(int(s[0]),'08X')
            litaral_entry(int(s[0]),"int",x)
            x = rev_big(x)
            return insop + x + "$#imm"

    if(s[0] in r32 and s[1] in r32):
        insop = search_ins_opcode(ins,["r32","r32"])
        ind1 = r32.index(s[0])
        ind2 = r32.index(s[1])
        x = mod[3] + opcode[ind2] + opcode[ind1]
        oprop = cal_opr_opcode(x)
        return insop + oprop + '$#reg32_' + str(ind1+1) + ',#reg32_' + str(ind2+1)

    if(s[0] in r16 and s[1] in r16):
        insop = search_ins_opcode(ins,["r16","r16"])
        ind1 = r16.index(s[0])
        ind2 = r16.index(s[1])
        x = mod[3] + opcode[ind2] + opcode[ind1]
        oprop = cal_opr_opcode(x)
        return insop+oprop + '$#reg16_' + str(ind1+1) + ',#reg16_' + str(ind2+1)

    if(s[0] in r8 and s[1] in r8):
        insop = search_ins_opcode(ins,["r8","r8"])
        ind1 = r8.index(s[0])
        ind2 = r8.index(s[1])
        x = mod[3] + opcode[ind2] + opcode[ind1]
        oprop = cal_opr_opcode(x)
        return insop+oprop + '$#reg8_' + str(ind1+1) + ',#reg8_' + str(ind2+1)
    
    if(s[0] in r32 and 'dword' in s[1]):
        insop = search_ins_opcode(ins,["r32","m32"])
        ind1 = r32.index(s[0])
        x = mod[0] + opcode[ind1] + "101" 
        oprop = cal_opr_opcode(x)
        sname = ((s[1].split('['))[1].split(']'))[0]
        sadd = lookup_symbol_add(sname)
        return insop + oprop + '[' + big_endian(sadd) + ']' + '$#reg32_'+str(ind1+1)+',#mem[sym_'+sname+']'

    if('dword' in s[0] and s[1] in r32):
        insop = search_ins_opcode(ins,["m32","r32"])
        ind1 = r32.index(s[1])
        x = mod[0] + opcode[ind1] + "101" 
        oprop = cal_opr_opcode(x)
        sname = ((s[0].split('['))[1].split(']'))[0]
        sadd = lookup_symbol_add(sname)
        return insop + oprop + '[' + big_endian(sadd) + ']' + '$#mem[sym_'+sname+'],#reg32_' + str(ind1+1)
        
    if(s[0] in r16 and 'word' in s[1]):
        insop = search_ins_opcode(ins,["r16","m16"])
        ind1 = r16.index(s[0])
        x = mod[0] + opcode[ind1] + "101" 
        oprop = cal_opr_opcode(x)
        sname = ((s[1].split('['))[1].split(']'))[0]
        sadd = lookup_symbol_add(sname)
        return insop + oprop + '[' + big_endian(sadd) + ']' + '$#reg8_'+str(ind1+1)+',#mem[sym_'+sname+']'
        
    if('word' in s[0] and s[1] in r16):
        insop = search_ins_opcode(ins,["m16","r16"])
        ind1 = r16.index(s[1])
        x = mod[0] + opcode[ind1] + "101" 
        oprop = cal_opr_opcode(x)
        sname = ((s[0].split('['))[1].split(']'))[0]
        sadd = lookup_symbol_add(sname)
        return insop + oprop + '[' + big_endian(sadd) + ']' + '$#mem[sym_'+sname+'],#reg16_' + str(ind1+1)
        
    if(s[0] in r8 and 'byte' in s[1]):
        insop = search_ins_opcode(ins,["r8","m8"])
        ind1 = r8.index(s[0])
        x = mod[0] + opcode[ind1] + "101" 
        oprop = cal_opr_opcode(x)
        sname = ((s[1].split('['))[1].split(']'))[0]
        sadd = lookup_symbol_add(sname)
        return insop + oprop + '[' + big_endian(sadd) + ']' + '$#reg8_'+str(ind1+1)+',#mem[sym_'+sname+']'
        
    if('byte' in s[0] and s[1] in r8):
        insop = search_ins_opcode(ins,["m8","r8"])
        ind1 = r8.index(s[1])
        x = mod[0] + opcode[ind1] + "101" 
        oprop = cal_opr_opcode(x)
        sname = ((s[0].split('['))[1].split(']'))[0]
        sadd = lookup_symbol_add(sname)
        return insop + oprop + '[' + big_endian(sadd) + ']' + '$#mem[sym_'+sname+'],#reg8_' + str(ind1+1)
        
    if(s[0] in r32 and s[1].isdigit() == True):
        insop = search_ins_opcode(ins,["r32","imm32"])
        x = format(int(s[1]),'08X')
        litaral_entry(int(s[1]),"int",x)
        x = rev_big(x)
        return insop + x + '$#reg32,#lit'
    
    if(s[0] in r16 and s[1].isdigit() == True):
        insop = search_ins_opcode(ins,["r16","imm16"])
        x = format(int(s[1]),'X')
        litaral_entry(int(s[1]),"int",x)
        x = rev_big(x)
        return insop + x + '$#reg16,#lit'
    
    if(s[0] in r8 and s[1].isdigit() == True):
        insop = search_ins_opcode(ins,["r8","imm8"])
        x = format(int(s[1]),'02X')
        litaral_entry(int(s[1]),"int",x)
        x = rev_big(x)
        return insop + x + '$#reg8,#lit'

    if("dword" in s[0] and s[1].isdigit() == True):
        insop = search_ins_opcode(ins,["m32","imm32"])
        x = format(int(s[1]),'08X')
        litaral_entry(int(s[1]),"int",x)
        x = rev_big(x)
        return insop + x + '$#mem32,#lit'
    
    if("word" in s[0] and s[1].isdigit() == True):
        insop = search_ins_opcode(ins,["m16","imm16"])
        x = format(int(s[1]),'X')
        litaral_entry(int(s[1]),"int",x)
        x = rev_big(x)
        return insop + x + '$#mem16,#lit'
    
    if("byte" in s[0] and s[1].isdigit() == True):
        insop = search_ins_opcode(ins,["m8","imm8"])
        x = format(int(s[1]),'02X')
        litaral_entry(int(s[1]),"int",x)
        x = rev_big(x)
        return insop + x + '$#mem8,#lit'

    if("dword" in s[0] and "dword" in s[1]):
        insop = search_ins_opcode(ins,["m32","m32"])
        return insop + '$#mem32,#mem32'
    
    if("word" in s[0] and "word" in s[1]):
        insop = search_ins_opcode(ins,["m16","m16"])
        return insop + '$#mem16,#mem16'
    
    if("byte" in s[0] and "byte" in s[1]):
        insop = search_ins_opcode(ins,["m8","m8"])
        return insop + '$#mem8,#mem8'

if __name__ == '__main__' :
    code = []
    mylst = []
    pass_1 = []

    sec = ['section .data','section .bss','section .text']
    dm = [' dd ',' db ',' dw ',' dq ']
    rm = [' resd ',' resb ',' resw ',' resq ']
    
    for line in fileinput.input("test.asm"):
        code.append(line)
    l_no = 1
    add = 0
    for i in range(len(code)):
        if (sec[0] in code[i] or sec[1] in code[i] or sec[2] in code[i]):
            mylst.append([index(l_no)," \t\t \t\t \t",code[i]])
            pass_1.append([index(l_no)," "," ","  ",code[i]])
            l_no += 1
            add = 0
        if dm[0] in code[i]:
            x = map(int,re.findall('\d+',code[i]))
            s_n = (code[i]).split()
            sym_entry(s_n[0],dm[0],"Defined",x,(len(x))*4,add)
            if len(x) > 0 :
                mylst.append([index(l_no)," ",address(add)," ",big_endian(x[0]),"\t\t",code[i]])
                pass_1.append([index(l_no)," "," ","  ",code[i]])
            add += (len(x))*4
            l_no += 1
        if dm[1] in code[i]:
            msg = code[i].split('\"')
            s_n = msg[0].split()
            msg = msg[1]+msg[2]
            msg = msg.replace(',','')
            msg = msg.replace('10','\n')
            sym_entry(s_n[0],dm[1],"Defined",msg,len(msg),add)
            n_t = len(msg)
            while n_t > 0 :
                n_t -= 9
                m_l = len(msg)/9
                if m_l == 0:
                    m_l = len(msg)
                else:
                    m_l = 9
                string = ''
                for j in range(m_l):
                    string += str(format(ord(str(msg[j])),'X'))
                string = string + '-'
                msg = msg[m_l:]
                mylst.append([index(l_no)," ",address(add)," ",string,"\t",code[i]])
                pass_1.append([index(l_no)," "," ","  ",code[i]])
                add += m_l
            l_no += 1
#       if dm[2] in code[i]:
#       if dm[3] in code[i]:
        if rm[0] in code[i]:
            x = map(int,re.findall('\d+',code[i]))
            y = format(x[0]*4,'X')
            mylst.append([index(l_no)," ",address(add)," <res ",bss_assem(y),">","\t\t",code[i]])
            pass_1.append([index(l_no)," "," ","  ",code[i]])
            s_n = code[i].split()
            sym_entry(s_n[0],rm[0],"Defined","notassign",4,add)
            add += (x[0])*4
            l_no += 1
        if rm[1] in code[i]:
            x = map(int,re.findall('\d+',code[i]))
            y = format(x[0],'X')
            mylst.append([index(l_no)," ",address(add)," <res ",bss_assem(y),">","\t\t",code[i]])
            pass_1.append([index(l_no)," "," ","  ",code[i]])
            s_n = code[i].split()
            sym_entry(s_n[0],rm[1],"Defined","notassign",x[0],add)
            add += x[0]
            l_no += 1
#        if rm[2] in code[i]:
#        if rm[3] in code[i]:
        if ("global" in code[i]) or ("extern" in code[i]):
            mylst.append([index(l_no),"      \t\t\t\t\t",code[i]])
            pass_1.append([index(l_no)," "," ","  ",code[i]])
            l_no += 1
        if ':' in code[i] :
            msg = code[i].split(':')
            sym_entry(msg[0],"func","Defined","notassign",0,add)
            mylst.append([index(l_no)," \t\t \t\t  \t",code[i]])
            pass_1.append([index(l_no)," "," ","  ",code[i]])
            l_no += 1
        else :
            ins = (code[i]).split()
            if len(ins) < 1:
                mylst.append([index(l_no),"\n"])
                pass_1.append([index(l_no)," "," ","  ",code[i]])
                l_no +=1
            elif ins[0] in op2 or ins[0] in op1 or ins[0] in op0:
                if len(ins) == 1:
                    op_c = gen_opcode(ins[0],[]) 
                elif "rep" in ins[0] :
                    op_c1 = gen_opcode(ins[0],[])
                    if len(ins) > 2 :
                        op_c2 = gen_opcode(ins[1],ins[2].split(','))
                    else:
                        op_c2 = gen_opcode(ins[1],[])
                    op_c1 = op_c1.split('$')
                    op_c = op_c1[0] + op_c2
                else:
                    oprands = ins[1].split(',')
                    op_c = gen_opcode(ins[0],oprands)
                opc = op_c.split('$')
                op_c = opc[0]
                mylst.append([index(l_no)," ",address(add)," ",op_c,"\t\t\t",code[i]])
                line = code[i].replace('\n',' ')
                pass_1.append([index(l_no)," "," ","  ",line," ",opc[1],'\n'])
                l_no += 1
                if '[' in op_c:
                    add += (len(op_c)/2)-1
                else:
                    add += (len(op_c)/2)


    new_fp = open('op.mylst','w+')
    for i in range(len(mylst)):
        new_fp.write(str(''.join(mylst[i])))
    sym_fp = open('symbol_table','w+')
    for i in sym_tab:
        sym_fp.write(str(i)+'\n')
    lit_fp = open('litarl_table','w+')
    for i in lit_tab:
        lit_fp.write(str(i)+'\n')

    pass_fp = open('pass_01','w+')
    for i in pass_1:
        pass_fp.write(str(''.join(i)))
