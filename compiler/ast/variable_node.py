from enum import Enum

from compiler.ast import ExprNode
from compiler.type import Type
from compiler.utils import InternalError

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
    EQ = 11
    NE = 12
    BIT_AND = 13
    BIT_XOR = 14
    BIT_OR = 15
    LOGIC_AND = 16
    LOGIC_OR = 17

class BinaryOpNode(ExprNode):
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
