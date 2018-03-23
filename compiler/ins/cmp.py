from compiler.ir import Instruction

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

    def replace_use(self, from, to):
        right = right.replace(from, to)
        if self.left != from:
            self.left = self.left.replace(from, to)
    def replace_def(self, from, to):
        self.left = self.left.replace(from, to)
    def replace_all(self, from, to):
        self.left = self.left.replace(from, to)
        self.right = self.right.replace(from, to)

    def calc_def_and_use(self):
        if isinstance(self.left, Reference):
            self.ddef |= self.left.get_all_ref()
        self.use |= self.left.get_all_ref()
        self.use |= self.right.get_all_ref()
        self.all_ref |= self.use
        self.all_ref |= self.ddef

    def __str__(self):
        return 'cmp ' + str(self.left) + ', ' + str(self.right)
