from compiler.ir import IR

class Jump(IR):
    label = None

    def __init__(self, label):
        self.label = label
    def accept(self, emitter):
        return emitter.visit(self)
