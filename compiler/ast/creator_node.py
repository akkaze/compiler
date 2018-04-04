from compiler.type import Type
from compiler.ast import ExprNode

class CreatorNode(ExprNode):
    location = None
    type = None
    exprs = []
    total = 0
    def __init__(self, loc, type, exprs, total):
        self.location = loc
        self.type = type
        self.exprs = exprs
        self.total = total

    @property
    def type(self):
        return self.type
    
    @property
    def location(self):
        return self.location
    def accept(self, visitor):
        return visitor.visit(self)
