from compiler.type import BoolType
from compiler.ast import LiteralNode

class BoolLiteralNode(LiteralNode):
    value = False

    def __init__(loc, value):
        super().__init__(loc, BoolType())
        self.value = value
    def accept(self, visitor):
        return visitor.visit(self)
