from compiler.ast import LHSNode


class ArefNode(LHSNode):

    def __init__(self, expr, index, type=None):
        self.expr = expr
        self.index = index
        self.type = type
        super().__init__()

    @property
    def is_multi_dimension(self):
        return isinstance(self.expr, ArefNode)

    @property
    def base_expr(self):
        if self.is_multi_dimension:
            return self.expr.base_expr
        else:
            return self.expr

    @property
    def location(self):
        return self.expr.location

    def accept(self, visitor):
        return visitor.visit(self)
