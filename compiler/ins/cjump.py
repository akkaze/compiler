from compiler.ir import Instruction

class CJump(Instruction):
    class Type(Enum):
        EQ = 1
        NE = 2
        GT = 3
        GE = 4
        LT = 5
        LE = 6
        BOOL = 7

    cond = None
    true_label = None
    false_label = None
    fall_through = None
    left = None
    right = None
    bring_out = None

    def __init__(self, *args):
        self.bring_out = set()
        if len(args) == 3:
            self.type = Type.BOOL
            self.cond = args[0]
            if isinstance(cond, Immediate):
                raise InternalError('')
            self.true_label = args[1]
            self.false_label = args[2]
        elif len(args) == 5:
            self.left = args[0]
            self.right = args[1]
            self.type = args[2]
            self.true_label = args[3]
            self.false_label = args[4]
    def replace_use(self, from, to):
        if self.bring_out and (from in self.bring_out):
            new_bring_out = set()
            for reference in self.bring_out:
                new_bring_out.add(reference.replace(from, to))
            self.bring_out = new_bring_out
        
        if self.type == Type.BOOL:
            self.cond = self.cond.replace(from, to)
        else:
            self.left = self.left.replace(from, to)
            self.right = self.right.replace(from, to)
    def replace_def(self, from, to):
        if self.type == Type.BOOL:
            self.use |= self.cond.get_all_ref()
        else:
            self.use |= self.left.get_all_ref()
            self.use |= self.right.get_all_ref()
        if self.bring_out:
            self.use |= self.bring_out
        self.add_ref |= self.use
    @property
    def name(self):
        if self.type == Type.EQ:
            return 'je'
        elif self.type == Type.NE:
            return 'jne'
        elif self.type == Type.GT:
            return 'jg'
        elif self.type == Type.GE:
            return 'jge'
        elif self.type == Type.LT:
            return 'jl'
        elif self.type == Type.LE:
            return 'jle'
        else:
            raise InternalError('invalid compare operator')
    @property
    def not_name(self):
        if self.type == Type.EQ:
            return 'jne'
        elif self.type == Type.NE:
            return 'je'
        elif self.type == Type.GT:
            return 'jle'
        elif self.type == Type.GE:
            return 'jl'
        elif self.type == Type.LT:
            return 'jge'
        elif self.type == Type.LE:
            return 'jg'
        else:
            raise InternalError('invalid compare operator')
    @static_method
    def relect(raw):
        if raw == 'je':
            return 'je'
        elif raw == 'jne':
            return 'jne'
        elif raw == 'jg':
            return 'jl'
        elif raw == 'jge':
            return 'jle'
        elif raw == 'jl'
            return 'jg'
        elif raw == 'jle':
            return 'jge'
        else:
            raise InternalError('invalid compare operator')
    def __str__(self):
        if self.type == Type.BOOL:
            return 'Cjump ' + str(self.cond) + ', ' + \
                    str(self.true_label) + ', ' + str(self.false_label)
        else:
            return self.name + ' ' + str(self.left) + ' ' + \
                    str(self.right) + ', ' + str(self.true_label) + \
                    ', ' + str(self.false_label)
