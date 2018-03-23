from compiler.ins import Instruction

class Label(Instruction):
    name = ''
    basic_block = None
    bring_use = None

    def __init__(self, name):
        self.bring_use = dict()
        self.name = name
    
    def replace_use(self, ffrom, to):
        pass
    
    def replace_def(self, ffrom, to):
        pass

    def replace_all(self, ffrom, to):
        self.replace_def(ffrom, to)

    def calc_def_and_use(self):
        pass
