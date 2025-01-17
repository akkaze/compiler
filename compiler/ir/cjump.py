from compiler.ir.ir import IR
from compiler.ir.label import Label


class CJump(IR):
    def __init__(self, cond, true_label, false_label):
        self.cond = cond
        assert isinstance(true_label, Label)
        assert isinstance(false_label, Label)
        self.true_label = true_label
        self.false_label = false_label

    def accept(self, emitter):
        return emitter.visit(self)

    def __repr__(self):
        return 'cjump {0}, {1}, {2}'.format(self.cond, self.true_label, self.false_label)
