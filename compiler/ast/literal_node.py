from compiler.type import Type
from compiler.ast import ExprNode

class LiteralNode(ExprNode):
    location = None
    type = None
    
    def __init__(self, loc, type):
        super().__init__()
        self.location = loc
        self.type = type

    @property
    def is_constant(self):
        return True
    
    @property
    def location(self):
        return self.location

    @property
    def type(self):
        return self.type
