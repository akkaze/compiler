from compiler.ir import Expr

class StrConst(Expr):
    entity = None

    def __init__(self, entity):
        self.entity = entity
    def accept(self, emitter):
        return emitter.visit(self)
