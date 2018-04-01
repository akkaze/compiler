from compiler.ins import Bin
class Mul(Bin):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.name = 'imul'
    def accept(self, translator):
        return translator.visit(self)
 
