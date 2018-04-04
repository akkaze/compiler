from compiler.ast import StmtNode, ExprNode, BlockNode

class ForNode(StmtNode):
    init = None
    cond = None
    incr = None
    body = None
    def __init__(self, loc, init, cond, incr, body):
        super().__init__(loc)
        self.init = init
        self.cond = cond
        self.incr = incr
        self.body = BlockNode.warp_block(body)
    def accept(self, visitor):
        return visitor.visit(self)
