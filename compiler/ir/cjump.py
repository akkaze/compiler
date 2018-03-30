from compiler.ir import IR

class CJump(IR):
    cond = None
    true_label = None
    false_label = None

    def __init__(self, cond, true_label, false_label):
        self.cond = cond
        self.true_label = true_label
        self.false_label = false_label
    def accept(self, emitter):
        return emitter.visit(self)
