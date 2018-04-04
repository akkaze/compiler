from compiler.ast import LHSNode

class ArefNode(LHSNode):
    expr = None
    index = None
    
    def __init__(self, expr, index, type = None):
        self.expr = expr
        self.index = inde
        if type:
            self.type = type
    
    @property
    def is_multi_dimension(self):
        return isinstance(self.expr, ArefNode)
    @property
    def base_expr(self):
        if self.is_multi_dimension():
            return expr.base_expr
        else:
            return expr
    def accept(self, visitor):
        return visitor.visit(self)
