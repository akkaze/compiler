from compiler.ast.literal_node import LiteralNode
from compiler.typ.integer_type import IntegerType


class IntegerLiteralNode(LiteralNode):
    def __init__(self, loc, value):
        super().__init__(loc, IntegerType())
        self.value = value
    def accept(self, visitor):
        return visitor.visit(self)
