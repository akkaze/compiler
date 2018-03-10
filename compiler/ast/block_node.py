from compiler.ast import StmtNode
from compiler.entity import Scope

class BlockNode(StmtNode):
    stmts = []
    scope = None

    def __init__(self, loc, stmts):
        super().__init__(loc)
        self.stmts = stmts
        self.stmts = stmts
    
    @staticmethod
    def warp_block(node):
        if not node:
            return None
        if isinstance(node, BlockNode):
            return node
        else:
            return BlockNode(node.location, [node])
