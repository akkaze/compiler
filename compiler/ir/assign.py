from  compiler.ir import IR

class Assign(IR):
    left = None
    right = None

    def __init__(self, left, right):
        self.left = left
        self.right = right
    def accept(self, emitter):
        return emitter.visit(self)
