from compiler.ast.stmt_node import StmtNode
from compiler.ast.block_node import BlockNode

class WhileNode(StmtNode):
    body = None
    cond = None
    def __init__(self, loc, cond, body):
        super().__init__(loc)
        self.cond = cond
        self.body = BlockNode.warp_block(body)
    def accept(self, visitor):
        return visitor.visit(self)
