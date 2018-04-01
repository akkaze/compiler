from compiler.ins import Bin
class Sub(Bin):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.name = 'sub'
    def accept(self, translator):
        return translator.visit(self)
 
