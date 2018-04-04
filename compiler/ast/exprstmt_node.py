from compiler.ast import StmtNode
from compiler.type import Type

class ExprStmtNode(StmtNode):
    expr = None
    def __init__(self, loc, expr):
        super().__init__(loc)
        self.expr = expr
    def accept(self, visitor):
        return visitor.visit(self)
