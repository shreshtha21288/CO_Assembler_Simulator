import sys 
# c=input()
class MEMORY:
    memory=[]
    def initialize(self):
        for line in sys.stdin:
            self.memory+=[line]
        if len(self.memory)<=255:
            empty_space=256-len(self.memory)
            while empty_space!=0:
                self.memory+=["0"*16]  
                empty_space=empty_space-1
    def getdata(self,prog_count):
        return self.memory[prog_count]
    def dump(self):
        for inst in self.memory:
            print(inst)
rf = {
                    "000": 0,               # R0
                    "001": 0,               # R1
                    "010": 0,               # R2
                    "011": 0,               # R3
                    "100": 0,               # R4
                    "101": 0,               # R5
                    "110": 0,               # R6
                    "FLAGS":"0"*16
                }

def execution(inst,rf,pc,var_mem):
    #inst contains the line,rf is the registers,pc is the program counter
    #je
    if inst[:5]=="01111":
        if rf["FLAGS"][-1]=="1":
            pc=int(inst[8:],2)
        else:
            pc+=1
        rf["FLAGS"]="0"*16 
    #jgt
    if inst[:5]=="01101":
        if rf["FLAGS"][-2]=="1":
            pc=int(inst[8:],2)
        else:
            pc+=1
        rf["FLAGS"]="0"*16  
    #jlt
    if inst[:5]=="01100":
        if rf["FLAGS"][-3]=="1":  
            pc=int(inst[8:],2)
        else:
            pc+=1
        rf["FLAGS"]="0"*16  
    #jmp
    if inst[:5]=="11111":
        pc=int(inst[8:],2)
        rf["FLAGS"]="0"*16
    #ld
    if inst[:5]=="10100":
        ch=str(int(inst[5:8],2))
        rf["FLAGS"]="0"*16
        pc+=1
        rf["R"+ch]=str[int(inst[8:],2)]
        var_mem+=str[int(inst[8:],2)]
        #update the var mem where var_mem is the list containing the memory for the variables
    #st
    if inst[:5]=="10101":
        ch=str(int(inst[5:8]),2)
        rf["FLAGS"]="0"*16
        pc+=1
        if str(int(inst[8:],2)) not in var_mem:
            var_mem+=str(int(inst[8:],2))
        i=var_mem.index(int(inst[8:],2))
        var_mem[i]=rf["R"+ch]
def add(self):
    r1=int(self[:3],2)
    r2=int(self[3:7],2)
    r3=int(self[7:10],2)
    r3=r2+r1 
    return bin(r3)
def sub(self):
    return 
def mul(self):
    return
def div(self):
    return
def checkOverflow(self):
    return
# def ExecutionEngine(self):
#     if self[:5]=="10000":
#         add(ins)
#         print("add")
#     elif self[:5]=="10001":
#         sub(ins)
#         print("subtract")
#     elif self[:5]=="10110":
#         mul(ins)
#         print("Multiply")
#     elif self[:5]=="10111":

#         print("Divide")
# ExecutionEngine(c)
if __name__=="__main__":
    p=add("000010011")
    print(p[2:])
