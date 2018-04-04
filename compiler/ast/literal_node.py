from compiler.type import Type
from compiler.ast import ExprNode

class LiteralNode(ExprNode):
    location = None
    type = None
    
    def __init__(self, loc, type):
        self.location = loc
        self.type = type
        super().__init__()

    @property
    def is_constant(self):
        return True
