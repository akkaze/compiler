from compiler.ins import Instruction
from compiler.ins.operand import Reference
class Bin(Instruction):
    left = None
    right = None

    def __init__(self, left, right):
        self.left = left
        self.right = right
        super().__init__()
    def replace_use(self, ffrom, to):
        self.right = self.right.replace(ffrom, to)
        if self.left != ffrom:
            self.left = self.left.replace(ffrom, to)

    def replace_def(self, ffrom, to):
        self.left = self.left.replace(ffrom, to)

    def replace_all(self, ffrom, to):
        self.left = self.left.replace(ffrom, to)
        self.right = self.right.replace(ffrom, to)

    def calc_def_and_use(self):
        if isinstance(self.left, Reference):
            self.m_ddef |= self.left.get_all_ref()
        self.m_use |= self.left.get_all_ref()
        self.m_use |= self.right.get_all_ref()
        self.m_all_ref |= self.m_use
        self.m_all_ref |= self.m_ddef

    def __str__(self):
        return self.name + ' ' + str(self.left) + ', ' + str(self.right)

    def __repr__(self):
        return self.name + ' ' + str(self.left) + ', ' + str(self.right)
