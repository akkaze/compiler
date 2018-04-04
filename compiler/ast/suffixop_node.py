from compiler.ast import UnaryOpNode

class SuffixOpNode(UnaryOpNode):
    def __init__(self, op, expr):
        super().__init__(op, expr)
    def accept(self, visitor):
        return visitor.visit(self)
