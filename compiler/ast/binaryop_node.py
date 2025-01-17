from enum import Enum

from compiler.ast.expr_node import ExprNode


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

    def __init__(self, left, op, right, type=None):
        super().__init__()
        self.operator = op
        self.left = left
        self.right = right
        self.m_type = type

    @property
    def location(self):
        return self.left.location

    @property
    def type(self):
        if self.m_type:
            return self.m_type
        else:
            return self.left.type

    @type.setter
    def type(self, value):
        self.m_type = value
        
    def accept(self, visitor):
        return visitor.visit(self)
