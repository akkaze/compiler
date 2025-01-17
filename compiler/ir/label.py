from compiler.ir.ir import IR

class Label(IR):

    def __init__(self, name = ''):
        assert isinstance(name, str)
        self.name = name
    def accept(self, emitter):
        return emitter.visit(self)
    def __repr__(self):
        return self.name