from enum import Enum
from compiler.ir import Expr

class Binary(Expr):
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


    left = None
    right = None
    operator = None
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    def accept(self, emitter):
        return emitter.visit(self)
