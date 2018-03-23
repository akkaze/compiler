from compiler.ir import Bin
class Sar(Bin):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.name = 'sar'
