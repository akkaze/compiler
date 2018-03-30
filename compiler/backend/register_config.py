from compiler.ins.operand import *

class RegisterConfig:
    rax = None
    rbx = None
    rcx = None
    rdx = None
    rsi = None
    rdi = None
    registers = None
    param_registers = None
    def __init__(self):
        self.registers = []
        self.param_registers = []
        rax = Register('rax', 'al')
        self.registers.append(rax)
        rbx = Register('rbx', 'bl')
        self.registers.append(rbx)
        rcx = Register('rcx', 'cl')
        self.registers.append(rcx)
        rdx = Register('rdx', 'dl')
        self.registers.append(rdx)
        rsi = Register('rsi', 'sil')
        self.registers.append(rsi)
        rdi = Register('rdi', 'dil')
        self.registers.append(rdi)
        rbp = Register('rbp', 'bpl')
        self.registers.append(rbp)
        rsp = Register('rsp', 'spl')
        self.registers.append(rsp)
        for i in range(8,16):
            self.registers.append(Register('r' + str(i),
                        'r' + str(i) + 'b'))
        callee_save = [1,6,12,13,14,15]
        for x in callee_save:
            self.registers[x].is_callee_save = True
        self.param_registers.append(rdi)
        self.param_registers.append(rsi)
        self.param_registers.append(rdx)
        self.param_registers.append(rcx)
        self.param_registers.append(self.registers[8])
        self.param_registers.append(self.registers[9])
