from compiler.ins import Instruction
from compiler.ins.operand import *

class Move(Instruction):
    dest = None
    src = None

    def __init__(self, dest, src):
        self.dest = dest
        self.src = src
        super().__init__()
    @property
    def is_ref_move(self):
        if isinstance(self.dest, Reference) and isinstance(self.src, Reference):
            type1 = self.src.type
            type2 = self.dest.type
            if (type1 == Reference.Type.UNKNOWN or \
                type1 == Reference.Type.REG) and \
                (type2 == Reference.Type.UNKNOWN or \
                type2 == Reference.Type.REG):
                return True
        return False

    def replace_use(self, ffrom, to):
        self.src = self.src.replace(ffrom, to)
        if not isinstance(self.dest, Reference):
            self.dest = self.dest.replace(ffrom, to)
    def replace_def(self, ffrom, to):
        self.dest = self.dest.replace(ffrom, to)

    def replace_all(self, ffrom, to):
        self.src = self.src.replace(ffrom, to)
        self.dest = self.dest.replace(ffrom, to)

    def calc_def_and_use(self):
        if isinstance(self.dest, Reference):
            self.m_ddef |= self.dest.get_all_ref()
            self.m_use |= self.src.get_all_ref()
        else:
            self.m_use |= self.dest.get_all_ref()
            self.m_use |= self.src.get_all_ref()
        self.m_all_ref |= self.m_use
        self.m_all_ref |= self.m_ddef

    def accept(self, translator):
        return translator.visit(self)
 
    def __str__(self):
        s =  'mov ' + str(self.dest) + ', ' + str(self.src)
        return s
