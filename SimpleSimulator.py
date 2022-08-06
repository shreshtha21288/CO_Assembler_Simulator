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
                self.memory+=["0*16"]  
                empty_space=empty_space-1
    def getdata(self,prog_count):
        return self.memory[prog_count]
    def dump(self):
        for inst in self.memory:
            print(inst)
registers = {
                    "000": 0,               # R0
                    "001": 0,               # R1
                    "010": 0,               # R2
                    "011": 0,               # R3
                    "100": 0,               # R4
                    "101": 0,               # R5
                    "110": 0,               # R6
                }
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
