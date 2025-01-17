from compiler.ast.stmt_node import StmtNode
from compiler.ast import block_node

class IfNode(StmtNode):
    cond = None
    then_body = None
    else_body = None
    def __init__(self, loc, cond, then_body, else_body):
        super().__init__(loc)
        self.cond = cond
        self.then_body = block_node.BlockNode.warp_block(then_body)
        self.else_body = block_node.BlockNode.warp_block(else_body)
    def accept(self, visitor):
        return visitor.visit(self)
