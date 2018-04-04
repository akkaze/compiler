from compiler.ast import StmtNode, ExprNode

class WhileNode(StmtNode):
    body = None
    cond = None
    def __init__(self, loc, cond, body):
        super().__init__(loc)
        self.cond = cond
        self.body = BlockNode.warp_block(body)
    def accept(self, visitor):
        return visitor.visit(self)
