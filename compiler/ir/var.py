from compiler.ir.expr import Expr

class Var(Expr):
    def __init__(self, entity):
        self.entity = entity
    def accept(self, emitter):
        return emitter.visit(self)
