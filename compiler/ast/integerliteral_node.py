from compiler.type import IntegerType
from compiler.ast import LiteralNode

class IntegerLiteralNode(LiteralNode):
    value = 0

    def __init__(self, loc, value):
        super().__init__(loc, IntegerType())
        self.value = value
    def accept(self, visitor):
        return visitor.visit(self)
