from compiler.ast import UnaryOpNode

class PrefixNode(UnaryOpNode):
    def __init__(self, op, expr):
        super().__init__(op, expr)
