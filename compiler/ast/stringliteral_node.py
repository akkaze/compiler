from compiler.type import StringType
from compiler.entity import StringConstantEntity
class BoolLiteralNode(LiteralNode):
    value = ''
    entity = None

    def __init__(loc, value):
        super().__init__(loc, StringType())
        self.value = value
