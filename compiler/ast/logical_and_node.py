from compiler.ast import BinaryOpNode


class LogicalAndNode(BinaryOpNode):
    def __init__(self, left, right):
        super().__init__(left, BinaryOpNode.BinaryOp.LOGIC_AND, right)

    def accept(self, visitor):
        return visitor.visit(self)
