from compiler.ins import Bin
class Sal(Bin):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.name = 'sal'
    def accept(self, translator):
        return translator.visit(self)
 
