from compiler.type import Type
from compiler.ast import ExprNode
from enum import Enum

class UnaryOp(Enum):
    PRE_INC = 1
    PRE_FEC = 2
    SUF_INC = 3
    SUF_DEC = 4
    MINUS = 5
    ADD = 6
    LOGIC_NOT = 7
    BIT_NOT = 8
class UnaryOpNode(ExprNode):
    operator = None
    expr = None
    type = None
    amount = 0
    
    def __init__(self, op, expr):
        self.operator = op
        self.expr = expr
        self.amount = 1
        super().__init__()

    @property
    def type(self):
        return self.expr.type

    @property
    def location(self):
        return self.expr.location
