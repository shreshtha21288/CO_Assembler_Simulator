import sys 

#MEMORY implementation 

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

# Program Counter Implementation

class PC:
    program_counter=0

    def initialize(self):
        self.program_counter=0
    def update(self,newcounter):
        self.program_counter=newcounter
    def dump(self):
        print(bin(self.program_counter)[2:])
    def getPC(self):
        return self.program_counter

# Register Implementation

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



def reg(inst):
    return rf[inst]
def update_register(value,index):
    rf[index]=value
def add(inst):
    r1=int(reg(inst[:3]),2)
    r2=int(reg(inst[3:6]),2)
    r3=int(reg(inst[7:10]),2)
    r3=r2-r1 
    value=bin(r3)[2:]
    return update_register(value,inst[7:10])
def sub(inst):
    r1=int(reg(inst[:3]),2)
    r2=int(reg(inst[3:6]),2)
    r3=int(reg(inst[7:10]),2)
    r3=r2-r1 
    value=bin(r3)[2:]
    return update_register(value,inst[7:10]) 
def mul(inst):
    r1=int(reg(inst[:3]),2)
    r2=int(reg(inst[3:7]),2)
    r3=int(reg(inst[7:10]),2)
    r3=r2*r1 
    return update_register(bin(r3),inst[7:10])
def div(inst):
    r1=int(reg(inst[:3]),2)
    r2=int(reg(inst[3:7]),2)
    r3=int(reg(inst[7:10]),2)
    r3=r2/r1 
    return update_register(bin(r3),inst[7:10])

# Execution Engine
class EE:

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
        if inst[:5]=="10000":
            add(inst)
            print("add")
        if inst[:5]=="10001":
            sub(inst)
            print("subtract")
        if inst[:5]=="10110":
            mul(inst)
            print("Multiply")
        if inst[:5]=="10111":
            div(inst)
            print("Divide")
def checkOverflow():
    return


if __name__=="__main__":
    MEMORY.initialize()
    inst=MEMORY.getdata()
