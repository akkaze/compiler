from compiler.type import FunctionType, Type
from compiler.ast import ExprNode

class FuncallNode(ExprNode):
    expr = None
    args = None
    def __init__(self, expr, args):
        self.expr = expr
        self.args = args
        super().__init__()

    def add_thispointer(self, expr):
        self.args.insert(0, expr)

    @property
    def type(self):
        return self.function_type.entity.return_type

    @property
    def function_type(self):
        return self.expr.type

    @property
    def location(self):
        return self.location
    
    def accept(self, visitor):
        return visitor.visit(self)
