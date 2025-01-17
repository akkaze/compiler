from compiler.ins import Instruction


class Label(Instruction):

    def __init__(self, name):
        self.bring_use = dict()
        self.basic_block = None
        self.name = name
        super().__init__()

    def replace_use(self, fffrom, to):
        pass

    def replace_def(self, fffrom, to):
        pass

    def replace_all(self, fffrom, to):
        self.replace_def(fffrom, to)

    def calc_def_and_use(self):
        pass

    def accept(self, translator):
        return translator.visit(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name