from compiler.type import BoolType

class BoolLiteralNode(LiteralNode):
    value = False

    def __init__(loc, value):
        super().__init__(loc, BoolType())
        self.value = value
