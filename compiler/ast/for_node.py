from compiler.ast.stmt_node import StmtNode
from compiler.ast import block_node
class ForNode(StmtNode):
    
    def __init__(self, loc, init, cond, incr, body):
        super().__init__(loc)
        self.init = init
        self.cond = cond
        self.incr = incr
        self.body = block_node.BlockNode.warp_block(body)
    def accept(self, visitor):
        return visitor.visit(self)
