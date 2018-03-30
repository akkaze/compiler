from compiler.ir import Expr

class Var(Expr):
    entity = None
    def __init__(self, entity):
        self.entity = entity
    def accept(self, emitter):
        return emitter.visit(self)
