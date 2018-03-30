from compiler.ir import Expr

class Call(Expr):
    entity = None
    args = []
    
    def __init__(self, entity, args):
        self.entity = entity
        self.args = args
    def accept(self, emitter):
        return emitter.visit(self)
