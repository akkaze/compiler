from compiler.ir import Expr

class Mem(Expr):
    expr = None

    def __init__(self, expr):
        self.expr = expr
    def accept(self, emitter):
        return emitter.visit(self)
