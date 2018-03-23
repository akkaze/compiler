from compiler.ins import Instruction

class Not(Instruction):
    operand = None
    def __init__(self, operand):
        self.operand = operand
    def replace_use(self, from, to):
        if not isinstance(self.operand, Reference):
            self.operand = self.operand.replace(from, to)
    def replace_def(self, from, to):
        if isinstance(self.operand, Reference):
            self.operand = self.operand.replace(from, to)
    def replace_all(self, from, to):
        self.operand = self.operand.replace(from, to)
    def calc_def_and_use(self):
        if isinstance(self.operand, Reference):
            self.ddef |= self.operand.get_all_ref()
        self.use |= self.operand.get_all_ref()
        self.all_ref |= self.use
        self.all_ref |= self.ddef
    def __str__(self):
        return 'not ' + str(self.operand) 
