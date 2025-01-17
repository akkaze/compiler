from compiler.ast.expr_node import ExprNode

class LiteralNode(ExprNode):
    
    def __init__(self, loc, type):
        self.location = loc
        self.type = type
        super().__init__()

    @property
    def is_constant(self):
        return True
