from compiler.ins import Instruction

class Lea(Instruction):
    dest = None
    addr = None
    def __init__(self, dest, addr):
        self.dest = dest
        self.addr = addr
    def replace_use(self, from, to):
        self.addr = self.addr.replace(from, to)
        if self.dest != self.from:
            self.dest = self.dest.replace(from, to)
    def replace_def(self, from, to):
        self.dest = self.dest.replace(from, to)
    def replace_all(self, from, to):
        self.addr = self.addr.replace(from, to)
        self.dest = self.dest.replace(from, to)
    def calc_def_and_use(self):
        if isinstance(self.dest, Reference):
            self.ddef |= self.dest.get_all_ref()
        self.use |= self.addr.get_all_ref()
        self.all_ref |= self.use
        self.all_ref |= self.ddef
    def __str__(self):
        return 'lea ' + str(dest) + ', ' + str(addr)
