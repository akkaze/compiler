from compiler.ir import Bin

class Move(Instruction):
    dest = None
    src = None

    def __init__(self, dest, src):
        self.dest = dest
        self.src = src
    @property
    def is_ref_move(self):
        if isinstance(self.dest, Reference) and \
            isinstance(self.src, Reference):
            type1 = self.src.type
            type2 = self.dest.typee
            if type1 == Reference.Type.UNKNOWN and \
                type1 == Reference.Type.REG and \
                type2 == Reference.Type.UNKNOWN and \
                type2 == Reference.Type.REG:
                return True
        return False

    def replace_use(self, from, to):
        self.src = self.src.replace(from, to)
        if not isinstance(dest, Reference):
            self.dest = self.dest.replace(from, to)
    def replace_def(self, from, to):
        self.dest = self.dest.replace(from, to)

    def replace_all(self, from, to):
        self.src = self.src.replace(from, to)
        self.dest = self.dest.replace(from, to)

    def calc_def_and_use(self):
        if isinstance(self.dest, Reference):
            self.ddef |= self.dest.get_all_ref()
            self.ddef |= self.src.get_all_ref()
        else:
            self.use |= self.dest.get_all_ref()
            self.use |= self.src.get_all_ref()
        self.add_ref |= self.use
        self.all_ref |= self.ddef

    def __str__(self):
        return 'mov ' + str(dest) + ', ' + str(src)
