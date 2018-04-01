from compiler.ins import Instruction
from enum import Enum
class Cmp(Instruction):
    class Operator(Enum):
        EQ = 1
        NE = 2
        GE = 3
        GT = 4
        LE = 5
        LT = 6
    left = None
    right = None
    operator = None

    def __init__(self, left, right, operator):
        self.left = left
        self.right = right
        self.operator = operator
        super().__init__()

    def replace_use(self, ffrom, to):
        right = right.replace(ffrom, to)
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

    def accept(self, translator):
        return translator.visit(self)
 
    def __str__(self):
        return 'cmp ' + str(self.left) + ', ' + str(self.right)
