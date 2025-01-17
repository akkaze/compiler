from compiler.ir import Expr


class IntConst(Expr):
    def __init__(self, value):
        assert isinstance(value, int)
        self.value = value

    def accept(self, emitter):
        return emitter.visit(self)
