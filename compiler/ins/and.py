from compiler.ir import Bin
class IR(Bin):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.name = 'and'
