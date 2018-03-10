from compiler.ast import StmtNode

class ReturnNode(StmtNode):
    expr = None
    
    def __init__(loc, expr):
        super().__init__(loc)
        self.expr = expr
