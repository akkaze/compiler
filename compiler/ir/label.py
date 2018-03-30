from compiler.ir import IR

class Label(IR):
    name = ''
    def __init__(self, name = ''):
        self.name = name
    def accept(self, emitter):
        return emitter.visit(self)
