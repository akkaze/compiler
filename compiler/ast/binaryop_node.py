from enum import Enum

from compiler.ast import ExprNode
from compiler.type import Type

class BinaryOpNode(ExprNode):
    class BinaryOp(Enum):
        ADD = 1
        SUB = 2
        MUL = 3
        DIV = 4
        MOD = 5
        LSHIFT = 6
        RSHIFT = 7
        LT = 8
        GT = 9
        LE = 10
        GE = 11
        EQ = 12
        NE = 13
        BIT_AND = 14
        BIT_XOR = 15
        BIT_OR = 16
        LOGIC_AND = 17
        LOGIC_OR = 18


    operator = None
    left = None
    right = None
    type = None
    
    def __init__(self, left, op, right, type = None):
        super().__init__()
        self.operator = op
        self.left = left
        self.right = right    
        self.type = type
    @property
    def location(self):
        return self.left.location
    def accept(self, visitor):
        return visitor.visit(self)
