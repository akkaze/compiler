from compiler.typ.string_type import StringType
from compiler.ast.literal_node import LiteralNode
from compiler.entity.string_const_entity import StringConstEntity


class StringLiteralNode(LiteralNode):
    value = ''
    entity = None

    def __init__(self, loc, value):
        super().__init__(loc, StringType())
        self.value = value

    def accept(self, visitor):
        return visitor.visit(self)
