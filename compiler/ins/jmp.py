from compiler.ins import Instruction

class Jmp(Instruction):
    dest = None
    def __init__(self, dest):
        self.dest = dest
        super().__init__()
    def replace_use(self, ffrom, to):
        pass
    def replace_def(self, ffrom, to):
        pass
    def calc_def_and_use(self):
        pass
    def accept(self, translator):
        return translator.visit(self)
 
    def __str__(self):
        return 'jmp ' + str(self.dest)

    def __repr__(self):
        return 'jmp ' + str(self.dest)
