from compiler.ins import Instruction

class Pop(Instruction):
    operand = None
    def __init__(self, operand):
        self.operand = operand
        super.__init__()
    def replace_use(self, ffrom, to):
        self.operand = self.operand.replace(ffrom, to)
    def replace_def(self, ffrom, to):
        self.operand = self.operand.replace(ffrom, to)
    def replace_all(self, ffrom, to):
        self.operand = self.operand.replace(ffrom, to)
    def calc_def_and_use(self):
        self.m_ddef |= self.operand.get_all_ref()
        self.m_all_ref |= self.m_use
    
    def accept(self, translator):
        return translator.visit(self)
 
    def __str__(self):
        return 'pop ' + str(self.operand)
