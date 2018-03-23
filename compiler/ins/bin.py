from compiler.ins import Instruction

class Bin(Instruction):
    left = None
    right = None

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def replace_use(self, from, to):
        self.right = self.right.replace(from, to)
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
        return self.name + ' ' + str(self.left) + ', ' + str(self.right)
