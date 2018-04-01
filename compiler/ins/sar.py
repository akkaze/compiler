from compiler.ins import Bin
class Sar(Bin):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.name = 'sar'
    def accept(self, translator):
        return translator.visit(self)
 
