from compiler.typ.function_type import FunctionType
from compiler.ast.expr_node import ExprNode


class FuncallNode(ExprNode):

    def __init__(self, expr, args):
        super().__init__()
        self.expr = expr
        self.args = args
        
    def add_thispointer(self, expr):
        assert isinstance(expr, ExprNode)
        self.args.insert(0, expr)

    @property
    def type(self):
        return self.function_type.entity.return_type

    @property
    def function_type(self):
        return self.expr.type

    @property
    def location(self):
        return self.expr.location

    @property
    def callee_name(self):
        return self.expr.entity.name
        
    def accept(self, visitor):
        return visitor.visit(self)

    def __str__(self):
        funcall_str =  str(self.expr) + '('
        for i, arg in enumerate(self.args):
            funcall_str += str(arg)
            if i != len(self.args) - 1:
                funcall_str += ','
        return funcall_str
