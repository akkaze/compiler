from compiler.ins.operand import Operand

class Register(Operand):
    name = ''
    low_name = ''
    is_callee_save = False

    def __init__(self, name, low_name):
        self.name = name
        self.low_name = low_name
    @property
    def is_caller_save(self):
        return not self.is_callee_save
    
    @property
    def is_register(self):
        return True
    @property
    def is_direct(self):
        return True
    def replace(self, ffrom, to):
        return self
    def get_all_ref(self):
        return set()
    @property
    def nasm(self):
        return self.name
    def __str__(self):
        return self.name
