from compiler.ast.stmt_node import StmtNode
class BlockNode(StmtNode):
    def __init__(self, loc, stmts):
        super().__init__(loc)
        self.stmts = stmts
    
    @staticmethod
    def warp_block(node):
        if not node:
            return None
        if isinstance(node, BlockNode):
            return node
        else:
            return BlockNode(node.location, [node])
    def accept(self, visitor):
        return visitor.visit(self)
