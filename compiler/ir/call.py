from compiler.ir.expr import Expr

class Call(Expr):
    
    def __init__(self, entity, args):
        self.entity = entity
        self.args = args

    def accept(self, emitter):
        return emitter.visit(self)

    def __str__(self):
        call_str = 'Call ' + str(self.entity) + ' '
        for arg in self.args:
            call_str += str(arg)
            if arg != len(self.args) - 1:
                call_str += ', '
        return call_str