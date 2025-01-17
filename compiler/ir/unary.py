from enum import Enum
from compiler.ir import Expr
class Unary(Expr):
    class UnaryOp(Enum):
        MINUS = 1
        LOGIC_NOT = 2
        BIT_NOT = 3

    def __init__(self, op, expr):
        super().__init__()
        self.operator = op
        self.expr = expr
    def accept(self, emitter):
        return emitter.visit(self)
