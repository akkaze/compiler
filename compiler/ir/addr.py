from compiler.ir import Expr

class Addr(Expr):
    def __init__(self, entity):
       super().__init__()
       self.entity = entity
    def accept(self, emitter):
        return emitter.visit(self)
