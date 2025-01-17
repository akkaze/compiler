from compiler.ins import Instruction

class Return(Instruction):
    ret = None
    def __init__(self, ret):
        self.ret = ret
        super().__init__()
    def replace_use(self, ffrom, to):
        if self.ret:
            self.ret = self.ret.replace(ffrom, to)

    def replace_def(self, ffrom, to):
        pass

    def replace_all(self, ffrom, to):
        pass

    def calc_def_and_use(self):
        if self.ret:
            self.m_use |= self.ret.get_all_ref()
            self.m_all_ref |= self.m_use

    def accept(self, translator):
        return translator.visit(self)
 
    def __str__(self):
        if self.ret:
            return 'ret ' + str(self.ret)
        else:
            return 'ret'

    def __repr__(self):
        if self.ret:
            return 'ret ' + str(self.ret)
        else:
            return 'ret'