from compiler.ins import Instruction

class Push(Instruction):
    operand = None
    def __init__(self, operand):
        self.operand = operand
    def replace_use(self, from, to):
        self.operand = self.operand.replace(from, to)
    def replace_def(self, from, to):
        self.operand = self.operand.replace(from, to)
    def replace_all(self, from, to):
        self.operand = self.operand.replace(from, to)
    def calc_def_and_use(self):
        self.use |= self.operand.get_all_ref()
        self.all_ref |= self.use
    def __str__(self):
        return 'push ' + str(self.operand)
