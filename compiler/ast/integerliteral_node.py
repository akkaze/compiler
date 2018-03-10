from compiler.type import IntegerType

class BoolLiteralNode(LiteralNode):
    value = 0

    def __init__(loc, value):
        super().__init__(loc, IntegerType())
        self.value = value
