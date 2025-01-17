from compiler.ast.stmt_node import StmtNode

class ExprStmtNode(StmtNode):
    def __init__(self, loc, expr):
        super().__init__(loc)
        self.expr = expr
    def accept(self, visitor):
        return visitor.visit(self)
