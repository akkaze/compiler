from compiler.ir.expr import Expr

class Mem(Expr):

    def __init__(self, expr):
        self.expr = expr
    def accept(self, emitter):
        return emitter.visit(self)
