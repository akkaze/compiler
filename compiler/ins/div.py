from compiler.ins import Bin
class Div(Bin):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.name = 'div'
