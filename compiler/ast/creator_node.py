from compiler.ast.expr_node import ExprNode

class CreatorNode(ExprNode):
    
    def __init__(self, loc, type, exprs, total):
        super().__init__()
        self.location = loc
        self.type = type
        self.exprs = exprs
        self.total = total

    # @property
    # def type(self):
    #     return self.type
    
    # @property
    # def location(self):
    #     return self.location
    def accept(self, visitor):
        return visitor.visit(self)
