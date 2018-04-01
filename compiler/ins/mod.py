from compiler.ins import Bin
class Mod(Bin):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.name = 'mod'
    def accept(self, translator):
        return translator.visit(self)
 
