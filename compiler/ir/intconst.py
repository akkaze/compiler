from compiler.ir import Expr

class IntConst(Expr):
    value = 0

    def __init__(self, value):
        self.value = value
    def accept(self, emitter):
        return emitter.visit(self)
