from compiler.ast import ExprNode

class AssignNode(ExprNode):
    lhs = None
    rhs = None
    
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    
    @property
    def type(self):
        return self.lhs.type
    
    @property
    def location(self):
        return self.lhs.location
    def accept(self, visitor):
        return visitor.visit(self)
