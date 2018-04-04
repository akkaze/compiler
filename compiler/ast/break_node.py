from compiler.ast import StmtNode

class BreakNode(StmtNode):
    def __init__(self, loc):
        super().__init__(loc)
    def accept(self, visitor):
        return visitor.visit(self)
