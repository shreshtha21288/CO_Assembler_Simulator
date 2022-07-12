# changes
import sys
var=[] #only one hlt instruction
label=[] 
imm=[]
pc=ins=lnum=0
t1={"mov":"10010", "rs":"11000", "ls":"11001"}
t2={"mov":"10011", "div":"10111", "not":"11101", "cmp":"11110"}
td={"ld" : "10100", "st" : "10101"}
te={"jmp" : "11111", "jlt" : "01100" ,"jgt" : "01101" , "je" :  "01111"}
reg={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
v={"R0" : "000" , "R1" : "001" , "R2" : "010" , "R3" : "011" , "R4" : "100",
    "R5" : "101" , "R6" : "110" , "FLAGS" : "111" }
q={     "add" : "10000" , 
    "sub" : "10001" , "mul" : "10110" , "xor" : "11010" , "or" : "11011" , 
    "and" : "11100"}
s=""            #output of the assembler
e=""            #error in the output
err_count=0     #line of error
err=0
ic=0            #no of instruction
hc=0            #give last halt command
hcc=0           #count no. of halt
count=0         #count the no of variable 
count_con=0     #count the no of variable defination consecutively 
lines=sys.stdin.readlines()
l_count=0
for line in lines:
    p=line.split()
    if len(p)!=0:
        if p[0]!="var" and p[0]!="hlt" and ":" not in p[0] and len(p)<3 and p[0] not in te:
                e="Incorrect instruction"
                err=1
                err_count=l_count
                break
        l_count+=1
    
for line in lines:
    if err==0:
        p=line.split()
        if len(p)!=0 and p[0]!="var":
            ins+=1
            if ":" in p[0]:
                i=p[0].index(":")
                if (len(p[0])-1) !=i:
                    err=1
                    e="label cannot have a character after colon"
                    break
                str1=p[0][0:i]
                label+=[[str1,ins-1,err_count]]
            if ":" in p:
                e="No spaces are allowed between label name and colon"  
                err=1  
                break
            if ":" in p[0] and "var" in p:
                e="Incorrect variable declartion inside a label"
                err=1
                break
            for str1 in p:
                if ":"  in str1:
                    lnum+=1
                if lnum>1:
                    e="One Label cannot be defined inside another label"
                    err=1
                    break
                else:
                    lnum=0
        if len(p)!=0:         
            err_count+=1
            if err==1:
                break
i_var=0       
for line in lines:
    if err==0:
        p=line.split()
        if len(p)==1 and p[0]=="var":
            err=1
            e="variable not declared"
            break
        if len(p)!=0 and p[0]=="var":
            var+=[[p[1],ins,i_var]]
            ins+=1
            i_var+=1
    else:
        break
for i in range(len(var)):
    if err==0:
        if len(var[i])!=3:
            err_count=var[i][2]
            e="Invalid instruction for variable declaration"
            err=1
            break
        if var[i][0].isdigit()==True:
            e="Variable name cannot be all digits"
            err_count=var[i][2]
            err=1
            break
        if  var[i][0][0] in ["0","1","2","3","4","5","6","7","8","9"]:
            e="Variable name cannot start with a digit"
            err_count=var[i][2]
            err=1
            break
        if var[i][0].isalnum()==False:
            e="Variable name is not alphanumeric" 
            err_count=var[i][2] 
            err=1
            break
        if var[i][0] in ["add","sub","mov","ld","st","mul","div","rs","ls","xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt"]:
            e="Variable name cannot be same as instruction name" 
            err_count=var[i][2]
            err=1
            break
l=[]   
for i in range(len(label)):
    if err==0:
        if label[i][0].isdigit()==True:
            err_count=label[i][2]
            e="Label name cannot be all digits"
            err=1
            break
        if label[i][0].isalnum()==False:
            err_count=label[i][2]
            e="Label name is not alphanumeric"  
            err=1
            break
        if label[i][0] in ["add","sub","mov","ld","st","mul","div","rs","ls","xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt"]:
            err_count=label[i][2]
            e="Label name cannot be same as instruction name" 
            err=1
            break 
        l+=[label[i][0]]
if len(set(l))!=len(l):
    e="Label names are not distinct"
    err=1       
dvar={v[0]: v[1] for v in var}
dlabel={l[0]: l[1] for l in label}
var_count=0         #count the line no. of last variable
for line in lines:
    p=line.split()
    if len(p)!=0:
        ic=ic+1
        if p[0]=="var":
            count=count+1
            var_count=ic-1
        if p[0]=="hlt":
            hc=ic
            hcc=hcc+1
        elif len(p)==2 and ":" in p[0] and p[1]=="hlt":
            hc=ic
            hcc=hcc+1
for line in lines:
    p=line.split()
    if len(p)!=0:
        if p[0]=="var":
            count_con+=1
        else:
            break
if hcc>1:
    err=1
    e="multiple halt have been used"
if count_con!=count:  #generates error if variable is defined after the instruction
    err_count=var_count
    err=1
    e="variable defined after the instruction"
if ic> hc:
    err_count=hc-1
    err=1
    e="halt not defined as last instruction"
if hc==0:
    err_count=ic
    err=1
    e="halt not defined in the end"
imm_count=0
#Shrestha
for line in lines:
    if err==0:
        p=line.split()
        if len(p)==3:
            if p[0]=="mov" and "$" in p[2]:
                if p[2][0]!="$":
                    e="Immediate value must be declared starting with $"
                    err=1
                    break
                i=p[2][1:]
                if i.isdigit()==False:
                    e="immediate value cannot be a character"
                    err=1
                    break
                imm+=[[p[2][1:],imm_count]]
            elif p[0]=="mov" and p[2] not in reg and "$" not in p[2]:
                e="Immediate value cannot be declared without $"
                err=1  
                break  
        if len(p)==4 and ":" in p[0]:
            if p[1]=="mov" and "$" in p[3]:
                if p[3][0]!="$":
                    e="Immediate value must be declared starting with $"
                    err=1
                    break
                i=p[3][1:]
                if i.isdigit()==False:
                    e="immediate value cannot be a character"
                    err=1
                    break
                imm+=[[p[3][1:],imm_count]]
            elif p[1]=="mov" and p[3] not in reg and "$" not in p[3]:
                e="Immediate value cannot be declared without $"
                err=1   
                break 
        if len(p)!=0:
            imm_count+=1
            if err==1:
                err_count=imm_count
                break
imm_list=[]
for i in imm:
    imm_list+=[i[0]]
for i in imm:
    if int(i[0])>255 or int(i[0])<0:
            err=1
            err_count=i[1]
            e="illegal immediate value, more than 8 bits"
            break


line_count=0
for line in lines:
    p=line.split()
    if err==1:
        break
    op=""
    if len(p)!=0:
        if ":" in p[0]:
            a=p[0]
            lb=a[:len(a)-1]
            if lb in dlabel:
                if p[1] in q :  #ignoring the empty lines between the input file
                    if len(p)==5:
                        op=op+q.get(p[1])
                        op=op+"00"
                        for i in range(2,len(p)):
                            if p[i] == "FLAGS": #FLAG error assertion
                                err=1
                                err_count=line_count
                                e="Illegal use of Flag"
                                break
                            if p[i] in v:
                                op=op+v.get(p[i])
                            else:
                                err=1
                                err_count=line_count
                                e="registor not defined"
                                break
                        s=s+op+"\n"
                    else:
                        err=1
                        err_count=line_count
                        e="syntax error"
                        break
            elif ":" in p[0] and lb not in dlabel:
                err=1
                err_count=line_count
                e="Label not defined"
                break
            elif ":" in p[0] and lb in dvar:
                err=1
                err_count=line_count
                e="misuse of variables as labels"
                break
        if p[0] in td:
                if len(p)==3:
                    if p[1] in reg and p[1]!="FLAGS":
                        op+=td.get(p[0])+reg.get(p[1])
                        if p[2] in dvar:
                            b=bin(dvar.get(p[2]))
                            op+=str(b)[2:].zfill(8)
                            s+=op+"\n"
                        elif p[2] in dlabel:
                            err_count=line_count
                            e="misuse of label as variable"
                            err=1 
                            break    
                        else:
                            err_count=line_count
                            e="Variable was not defined"
                            err=1
                            break
                    elif p[1]=="FLAGS":
                        err_count=line_count
                        e="This operation is not allowed on FLAGS"  
                        err=1 
                        break
                    else:
                        err_count=line_count
                        e="register not defined"      
                        err=1 
                        break
                else:
                    err_count=line_count
                    e="Syntax Error"
                    err=1
                    break
        if len(p)>1:
            if p[1] in td:            
                if len(p)==4 and ":" in p[0]:
                    if p[2] in reg and p[2] !="FLAGS":
                        op+=td.get(p[1])+reg.get(p[2])
                        if p[3] in dvar:
                            b=bin(dvar.get(p[3]))
                            op+=str(b)[2:].zfill(8)
                            s+=op+"\n"
                        elif p[3] in dlabel:
                            err_count=line_count
                            e="misuse of label as variable"
                            err=1 
                            break
                        else:
                            err_count=line_count
                            e="Variable was not defined"
                            err=1
                            break
                    elif p[2]=="FLAGS":
                        err_count=line_count
                        e="This operation is not allowed on FLAGS"  
                        err=1 
                        break
                    else:
                        err_count=line_count
                        e="register not defined"      
                        err=1 
                        break       
                else:
                    err_count=line_count
                    e="Syntax Error"
                    err=1 
                    break
        if p[0] in te:
            if len(p)==2:
                op+=te.get(p[0])+"000"
                if p[1] in dlabel:
                    b=bin(dlabel.get(p[1]))
                    op+=str(b)[2:].zfill(8)
                    s+=op+"\n"
                elif p[1] in dvar:
                    err_count=line_count
                    e="misuse of variable as label"
                    err=1 
                    break   
                else:
                    err_count=line_count
                    e="label was not defined"
                    err=1
                    break
            else:
                err_count=line_count
                e="Syntax Error"
                err=1 
                break
        if p[0] in q:  #ignoring the empty lines between the input file
                if len(p)==4:
                    op=op+q.get(p[0])
                    op=op+"00"
                    for i in range(1,len(p)):
                        if p[i] == "FLAGS": #FLAG error assertion
                            err=1
                            err_count=line_count
                            e="Illegal Use of Flag"
                            break
                        if p[i] in v:
                            op=op+v.get(p[i])
                        else:
                            err=1
                            err_count=line_count
                            e="register not defined"
                    s=s+op+"\n"
                else:
                    err_count=line_count
                    e="Syntax error"
                    err=1
                    break
        if len(p)==1 and p[0]=="hlt":
            op="0101000000000000"
            s+=op+"\n"  
        if len(p)>1 and p[0]=="hlt":
            err_count=line_count
            e="Incorrect hlt instruction"
            err=1
        if len(p)==2 and ":" in p[0] and p[1]=="hlt":
            op="0101000000000000"
            s+=op+"\n"
    if len(p)>=3 :
        if p[0] in t1 and p[2] not in reg:
            if len(p)==3:
                op+=t1.get(p[0])
                if p[1] in reg and p[1]!="FLAGS":
                    op+=reg.get(p[1])
                    if p[2][1:] in imm_list:
                        b=bin(int(p[2][1:]))
                        op+=str(b)[2:].zfill(8)
                        s+=op+"\n"
                    else:
                        err_count=line_count
                        e="immediate value not found"
                        err=1
                        break
                elif p[1]=="FLAGS":
                    err_count=line_count
                    e="This operation is not allowed on FLAGS"
                    err=1
                    break    
                else:
                    err_count=line_count
                    e="register not defined"
                    err=1
                    break
            else:
                err_count=line_count
                e="syntax error"
                err=1
                break
        if p[0] in t2 and p[2] in reg:
            if len(p)==3:
                op+=t2.get(p[0])
                op+="00000"
                if p[1] in reg :
                    op+=reg.get(p[1])
                    if p[2] in reg and p[2]!="FLAGS":
                        op+=reg.get(p[2])
                        s+=op+"\n"
                    elif p[2]=="FLAGS":
                        err_count=line_count
                        e="This operation is not allowed on FLAGS"
                        err=1
                        break
                    else:
                        err_count=line_count
                        e="register not defined"
                        err=1
                        break
                else:
                    err_count=line_count
                    e="register not defined"
                    err=1
                    break
            else:
                err_count=line_count
                e="syntax error"
                err=1
                break
        if p[1] in t1 and p[3] not in reg:
            if len(p)==4 and ":" in p[0]:
                op+=t1.get(p[1])
                if p[2] in reg and p[2]!="FLAGS":
                    op+=reg.get(p[2])
                    if p[3][1:] in imm_list:
                        b=bin(int(p[3][1:]))
                        op+=str(b)[2:].zfill(8)
                        s+=op+"\n"
                    else:
                        err_count=line_count
                        e="immediate value not found"
                        err=1
                        break
                elif p[2]=="FLAGS":
                    err_count=line_count
                    e="This operation is not allowed on FLAGS"
                    err=1
                    break    
                else:
                    err_count=line_count
                    e="register not defined"
                    err=1
                    break
            else:
                err_count=line_count
                e="syntax error"
                err=1
                break
        if p[1] in t2 and p[3] in reg:
            if len(p)==4 and ":" in p[0]:
                op+=t2.get(p[1])
                op+="00000"
                if p[2] in reg :
                    op+=reg.get(p[2])
                    if p[3] in reg and p[3]!="FLAGS":
                        op+=reg.get(p[3])
                        s+=op+"\n"
                    elif p[3]=="FLAGS":
                        err_count=line_count
                        e="This operation is not allowed on FLAGS"
                        err=1
                        break 
                    else:
                        err_count=line_count
                        e="register not defined"
                        err=1
                        break   
                else:
                    err_count=line_count
                    e="register not defined"
                    err=1
                    break
            else:
                err_count=line_count
                e="syntax error"
                err=1
                break
    if len(p)!=0:
        line_count+=1
        if err==1:
            break
if err==0:
    print(s)
else:
    print(f"ERROR @ line {err_count} :",e)
