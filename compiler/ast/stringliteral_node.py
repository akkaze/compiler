from compiler.type import StringType
from compiler.ast import LiteralNode
from compiler.entity import StringConstantEntity

class StringLiteralNode(LiteralNode):
    value = ''
    entity = None

    def __init__(loc, value):
        super().__init__(loc, StringType())
        self.value = value
    def accept(self, visitor):
        return visitor.visit(self)
