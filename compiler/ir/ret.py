from compiler.ir import IR

class Return(IR):
    expr = None

    def __init__(self, expr):
        self.expr = expr
    def accept(self, emitter):
        return emitter.visit(self)
