from compiler.ins import Instruction
from enum import Enum

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
            self.type = CJump.Type.BOOL
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
        super().__init__()
    def replace_use(self, ffrom, to):
        if self.bring_out and (ffrom in self.bring_out):
            new_bring_out = set()
            for reference in self.bring_out:
                new_bring_out.add(reference.replace(ffrom, to))
            self.bring_out = new_bring_out
        
        if self.type == CJump.Type.BOOL:
            self.cond = self.cond.replace(ffrom, to)
        else:
            self.left = self.left.replace(ffrom, to)
            self.right = self.right.replace(ffrom, to)
    def replace_def(self, ffrom, to):
        pass
    def calc_def_and_use(self):
        if self.type == CJump.Type.BOOL:
            self.m_use |= self.cond.get_all_ref()
        else:
            self.m_use |= self.left.get_all_ref()
            self.m_use |= self.right.get_all_ref()
        if self.bring_out:
            self.m_use |= self.bring_out
        self.m_all_ref |= self.m_use
    @property
    def name(self):
        if self.type == CJump.Type.EQ:
            return 'je'
        elif self.type == CJump.Type.NE:
            return 'jne'
        elif self.type == CJump.Type.GT:
            return 'jg'
        elif self.type == CJump.Type.GE:
            return 'jge'
        elif self.type == CJump.Type.LT:
            return 'jl'
        elif self.type == CJump.Type.LE:
            return 'jle'
        else:
            raise InternalError('invalid compare operator')
    @staticmethod
    def not_name(raw):
        if raw == 'je':
            return 'jne'
        elif raw == 'jne':
            return 'je'
        elif raw == 'jg':
            return 'jle'
        elif raw == 'jge':
            return 'jl'
        elif raw == 'jl':
            return 'jge'
        elif raw == 'jle':
            return 'jg'
        else:
            raise InternalError('invalid compare operator')

    @staticmethod
    def relect(raw):
        if raw == 'je':
            return 'je'
        elif raw == 'jne':
            return 'jne'
        elif raw == 'jg':
            return 'jl'
        elif raw == 'jge':
            return 'jle'
        elif raw == 'jl':
            return 'jg'
        elif raw == 'jle':
            return 'jge'
        else:
            raise InternalError('invalid compare operator')
    def accept(self, translator):
        return translator.visit(self)
 
    def __str__(self):
        if self.type == CJump.Type.BOOL:
            return 'Cjump ' + str(self.cond) + ', ' + \
                    str(self.true_label) + ', ' + str(self.false_label)
        else:
            return self.name + ' ' + str(self.left) + ' ' + \
                    str(self.right) + ', ' + str(self.true_label) + \
                    ', ' + str(self.false_label)
