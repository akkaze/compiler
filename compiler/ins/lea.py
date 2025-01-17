from compiler.ins import Instruction
from compiler.ins.operand.reference import Reference
class Lea(Instruction):
    def __init__(self, dest, addr):
        self.dest = dest
        self.addr = addr
        super().__init__()
    def replace_use(self, ffrom, to):
        self.addr = self.addr.replace(ffrom, to)
        if self.dest != ffrom:
            self.dest = self.dest.replace(ffrom, to)
    def replace_def(self, ffrom, to):
        self.dest = self.dest.replace(ffrom, to)
    def replace_all(self, ffrom, to):
        self.addr = self.addr.replace(ffrom, to)
        self.dest = self.dest.replace(ffrom, to)
    def calc_def_and_use(self):
        if isinstance(self.dest, Reference):
            self.m_ddef |= self.dest.get_all_ref()
        self.m_use |= self.addr.get_all_ref()
        self.m_all_ref |= self.m_use
        self.m_all_ref |= self.m_ddef
    def accept(self, translator):
        return translator.visit(self)
 
    def __str__(self):
        return 'lea ' + str(self.dest) + ', ' + str(self.addr)
