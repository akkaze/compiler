from compiler.ast import UnaryOpNode

class SuffixNode(UnaryOpNode):
    def __init__(self, op, expr):
        super().__init__(op, expr)
