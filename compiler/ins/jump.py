from compiler.ir import Bin

class Jump(Instruction):
    dest = None
    def __init__(self, dest):
        self.dest = dest
    def replace_use(self, from, to):
        pass
    def replace_def(self, from, to):
        pass
    def calc_def_and_use(self, from, to):
        pass
    def __str__(self):
        return 'jump ' + str(dest)
