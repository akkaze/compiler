from compiler.ins import Bin
class And(Bin):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.name = 'and'
    def accept(self, translator):
        return translator.visit(self)
 
