from compiler.ast import {StmtNode, ExprNode, BlockNode}

class WhileNode(StmtNode):
    cond = None
    then_body = None
    else_body = None
    def __init__(self, loc, cond, then_body, else_body):
        super().__init__(loc)
        self.cond = cond
        self.then_body = BlockNode.warp_block(then_body)
        self.else_body = BlockNode.warp_block(else_body)
