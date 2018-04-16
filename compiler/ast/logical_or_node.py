from compiler.ast import BinaryOpNode

class LogicalOrNode(BinaryOpNode):
    def __init__(self, left, right):
        super().__init__(left, BinaryOpNode.BinaryOp.LOGIC_OR, right)
    def accept(self, visitor):
        return visitor.visit(self)
