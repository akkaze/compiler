from compiler.typ.bool_type import BoolType
from compiler.ast.literal_node import LiteralNode


class BoolLiteralNode(LiteralNode):

    def __init__(self, loc, value):
        super().__init__(loc, BoolType())
        self.value = value

    def accept(self, visitor):
        return visitor.visit(self)
