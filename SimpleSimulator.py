from enum import Flag
import sys 

#MEMORY implementation 

class MEMORY:
    memory=[]
    def initialize(self):
        lines=sys.stdin.readlines()
        for line in lines:
            self.memory+=[line]
        if len(self.memory)<=255:
            empty_space=256-len(self.memory)
            while empty_space!=0:
                self.memory+=["0"*16]  
                empty_space=empty_space-1
    def getdata(self,prog_count):
        return self.memory[prog_count]

    def setValue(self,value,mem_addr):
        self.memory[mem_addr]=value
    def dump(self,var_mem):
        mem=[]
        for line in self.memory:
            mem+=line
        for line in var_mem:
            mem+=line
        for inst in mem:
            print(inst)

# Program Counter Implementation

class PC:
    program_counter=0
    def initialize(self):
        self.program_counter=0
    def update(self,newcounter):
        self.program_counter=newcounter
    def dump(self):
        print(bin(self.program_counter)[2:].zfill(8)," ")
    def getPC(self):
        return self.program_counter

# Register Implementation
class REG:
    r = {
                            "000": 0,               # R0
                            "001": 0,               # R1
                            "010": 0,               # R2
                            "011": 0,               # R3
                            "100": 0,               # R4
                            "101": 0,               # R5
                            "110": 0               # R6
                        }
    FLAG = "0000000000000000"
    # def initialize(self):
    #     self.rf
    def get_r(self):
        return self.r
    def resetFlag(self):
        self.FLAG="0"*16

    def O_Flag(self):
        self.FLAG = "0000000000001000"
    
    def L_Flag(self):
        self.FLAG = "0000000000000100"

    def G_Flag(self):
        self.FLAG = "0000000000000010"

    def E_Flag(self):
        self.FLAG = "0000000000000001"

    def update_register(self,value,index):
        self.r[index]=int(value,2)

    def dump(self):
        out=""
        for i in self.r:
            out+=bin(self.r[i])[2:].zfill(16)+" "
        out+=(self.FLAG)
        print(out)
    def getflag(self):
        return self.FLAG

rf=REG()
# rf.initialize()

def checkOverflow(r3):
    if r3>(2**16-1) and r3<0:
        return True
    else:
        return False

def reg(inst):
    r=rf.get_r()
    return bin(r[inst])[2:].zfill(16)


def add(inst):
    r1=int(reg(inst[7:10]),2)
    r2=int(reg(inst[10:13]),2)
    r3=int(reg(inst[13:16]),2)
    r3=r2+r1 
    if checkOverflow(r3):
        rf.O_Flag()
    else:
        rf.resetFlag()
    value=bin(r3)[2:].zfill(16)
    return rf.update_register(value,inst[13:16])
def sub(inst):
    r1=int(reg(inst[7:10]),2)
    r2=int(reg(inst[10:13]),2)
    r3=int(reg(inst[13:16]),2)
    r3=r2-r1 
    if checkOverflow(r3):
        rf.O_Flag()
    else:
        rf.resetFlag()
    value=bin(r3)[2:].zfill(16)
    return rf.update_register(value,inst[13:16]) 
def mul(inst):
    r1=int(reg(inst[7:10]),2)
    r2=int(reg(inst[10:13]),2)
    r3=int(reg(inst[13:16]),2)
    r3=r2*r1
    if checkOverflow(r3):
        rf.O_Flag()
    else:
        rf.resetFlag()
    value=bin(r3)[2:].zfill(16)
    return rf.update_register(value,inst[13:16]) 
def XOR(inst):
    r1=reg(inst[7:10])
    r2=reg(inst[10:13])
    r3=""
    for i in range(16):
        if r1[i] == r2[i]:
            r3+='0'
        else:
            r3+='1'
    return rf.update_register(r3,inst[13:16]) 
def OR(inst):
    r1=reg(inst[7:10])
    r2=reg(inst[10:13])
    r3=""
    for i in range(16):
        if r1[i] == '0' and r2[i] == '0':
            r3+='0'
        else:
            r3+='1'
    return rf.update_register(r3,inst[13:16])
def AND(inst):
    r1=reg(inst[7:10])
    r2=reg(inst[10:13])
    r3=""
    for i in range(16):
        if r1[i] == '1' and r2[i] == '1':
            r3+='1'
        else:
            r3+='0'
    return rf.update_register(r3,inst[13:16])
# Execution Engine
class EE:
    new_counter=0
    def execute(inst,rf,pc,mem,new_counter,halted):
        #inst contains the line,rf is the registers,pc is the program counter
        #je
        if inst[:5]=="01111":
            flag=rf.getflag()
            if flag[-1]=="1":
                new_counter=int(inst[8:],2)
                pc.update(new_counter)
            else:
                new_counter+=1
                pc.update(new_counter)
            rf.resetFlag() 
        #jgt
        if inst[:5]=="01101":
            flag=rf.getflag()
            if flag[-2]=="1":
                new_counter=int(inst[8:],2)
                pc.update(new_counter)
            else:
                new_counter+=1
                pc.update(new_counter)
            rf.resetFlag()  
        #jlt
        if inst[:5]=="01100":
            flag=rf.getflag()
            if flag[-3]=="1":  
                new_counter=int(inst[8:],2)
                pc.update(new_counter)
            else:
                new_counter+=1
                pc.update(new_counter)
            rf.resetFlag()  
        #jmp
        if inst[:5]=="11111":
            new_counter=int(inst[8:],2)
            pc.update(new_counter)
            rf.resetFlag()
        #ld
        if inst[:5]=="10100":
            ch=inst[5:8]
            mem_addr=int(inst[8:],2)
            rf.resetFlag()
            new_counter+=1
            pc.update(new_counter)
            val=mem.getdata(mem_addr)
            rf.update_register(ch,val)
            #update the var mem where var_mem is the list containing the memory for the variables
        #st
        if inst[:5]=="10101":
            ch=reg(inst[5:8])
            mem_addr=int(inst[8:],2)
            rf.resetFlag()
            new_counter+=1
            pc.update(new_counter)
            mem.setValue(ch,mem_addr)

        # if inst[:5]=="10010":
        #         flag=rf.getflag()
        #         if flag[-1]=="1":
        #                 new_counter=int(inst[8:],2)
        #                 pc.update(new_counter)
        #         else:
        #                 new_counter+=1
        #                 pc.update(new_counter)
        #         rf.resetFlag()
        #ls
        if inst[:5]=="11001":
                flag=rf.getflag()
                if flag[-2]=="1":
                        new_counter=int(inst[8:],2)
                        pc.update(new_counter)
                else:
                        new_counter+=1
                        pc.update(new_counter)
                rf.resetFlag()

        if inst[:5]=="10010":
            r1=inst[5:8:]       
            imm=inst[8::]        
            value=bin(int(imm,2))[2:].zfill(16)    
            rf.update_register(r1, value)
            new_counter+=1
            pc.update(new_counter)
            rf.resetFlag()
        #ls
        if inst[:5]=="11001":
            r1=reg(inst[5:8:])
            imm=int(inst[8::],2)
            shiftedString=r1[imm::] + '0' * imm
            new_counter+=1
            pc.update(new_counter)
            rf.update_register(shiftedString,inst[5:8])
            rf.resetFlag()
        #type C
        #mov reg
        if inst[:5]=="10011":
            r1=inst[10:13:]      
            r2=inst[13::]        
            new_counter+=1
            pc.update(new_counter)
            rf.update_register(r1,reg(r2))
            rf.resetFlag()
        #div
        if inst[:5]=="10111":
            r1=int(reg(inst[10:13:]),2)      
            r2=int(reg(inst[13::] ),2)       
            r=r1%r2
            q=r1//r2
            rf.update_register(q,"000")
            rf.update_register(r,"001")
            new_counter+=1
            pc.update(new_counter)
            rf.resetFlag()
        #rs
        if inst[:5]=="11000":
            r1=reg(inst[5:8:])
            imm=int(inst[8::],2)
            shiftedString=  '0' * imm + r1[:len(r1)-imm:]  
            new_counter+=1
            pc.update(new_counter)
            rf.update_register(shiftedString,inst[5:8])
            rf.resetFlag()
        #not
        if inst[:5]=="11101":
            r1=inst[10:13:]      
            r2=reg(inst[13::])       
            inv=""
            for bit in r2:
                if bit=='1':
                    inv+='0'
                else:
                    inv+='1'
            rf.update_register(r1, r2)
            new_counter+=1
            pc.update(new_counter)
            rf.resetFlag()
        #cmp
        if inst[:5]=="11110":
            r1=int(reg(inst[10:13:]),2)      
            r2=int(reg(inst[13::]),2)        
            if r1 < r2:
                rf.L_Flag()
            elif r1 > r2:
                rf.G_Flag()
            else:
                rf.E_Flag()
            new_counter+=1
            pc.update(new_counter)
        if inst[:5]=="10000":
            add(inst)
            new_counter+=1
            pc.update(new_counter)
            print("add")
        if inst[:5]=="10001":
            sub(inst)
            new_counter+=1
            pc.update(new_counter)
            print("subtract")
        if inst[:5]=="10110":
            mul(inst)
            new_counter+=1
            pc.update(new_counter)
            print("Multiply")
        if inst[:5]=="11010":
            XOR(inst)
            new_counter+=1
            pc.update(new_counter)
            print("Xor")
        if inst[5:]=="11011":
            OR(inst)
            new_counter+=1
            pc.update(new_counter)
            print("or")
        if inst[5:]=="11100":
            AND(inst)
            new_counter+=1
            pc.update(new_counter)
            print("And")
        if inst=="0101000000000000":
            halted=True
        return halted,pc.getPC()

    


if __name__=="__main__":
    var_mem={}
    rf=REG()
    # rf.initialize()
    mem=MEMORY()
    mem.initialize()
    Program_counter = PC()
    Program_counter.initialize()
    new_counter=0
    halted = False
    while halted==False:        
        Instruction = mem.getdata(Program_counter.getPC())
        halted, new_PC = EE.execute(Instruction,rf,Program_counter,mem,new_counter,halted)
        Program_counter.dump()
        rf.dump()
    mem.dump()
