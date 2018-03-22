class Reference(Operand):
    class Type(Enum):
        GLOBAL = 1
        OFFSET = 2
        REG = 3
        UNKNOWN = 4
        UNUNSED = 5
        CANNOT_COLOR = 6
        SPECIAL = 7

    type = None
    name = ''
    reg = None
    offset = 0
    entity = None
    ref_times = 0

    adj_list = None
    degree = 0
    alias = None
    color = None
    move_list = None
    is_precolored = False
    is_spilled = False

    def __init__(self, *args):
        self.move_list = set()
        self.adj_list = set()
        if len(args) == 2:
            if isinstance(args[0], str):
                self.name = args[0]
                self.type = args[1]
            else:
                self.set_offst(args[0], args[1])
        elif len(args) == 1:
            if isinstance(args[0], Register):
                self.set_register(args[0])
                self.name = args[0].name
            else:
                self.name = args[0].name
                self.entity = args[0]
                self.type = Type.UNKNOWN
    def reset(self):
        self.ref_times = 0
        self.move_list = set()
        self.adj_list = set()
        if not self.is_precolored:
            self.color = None
            self.degree = 0
        else:
            self.degree = sys.maxsize
        self.alias = None
        self.is_spilled = False
    def can_be_accumulator(self):
        return self.type == Type.UNKNOWN and self.entity is None

    def set_offset(self, offset, reg):
        self.offset = offset
        self.reg = reg
        self.type = Type.OFFSET
    def set_register(self, reg):
        self.reg = reg
        self.type = Type.REG
    @property
    def is_unknown(self):
        return self.type == Type.UNKNOWN and self.color is None

    def replace(self, from, to):
        if self == from:
            return to
        else:
            return self

    def __eq__(self, o):
        if isinstance(o, Reference):
            if self.type != o.type:
                return False
            if self.type == Type.REG:
                return self.reg == o.reg
            elif self.type == Type.OFFSET:
                return self.reg == o.reg and self.offset == o.offset
            elif self.type == Type.GLOBAL:
                return self.name == o.name
            else:
                raise InternalError('Unhandled cas in reference.eq')
        return False

    def get_all_ref(self):
        ret = set()
        if self.type != Type.GLOBAL and self.type != Type.CANNOT_COLOR \
            and self.type != SPECIAL:
            ret.add(self)
        return ret

    @property
    def is_register(self):
        return self.type == Type.REG
    @property
    def is_direct(self):
        return True
    @property
    def is_address(self):
        return self.type == Type.GLOBAL or \
            self.type == Type.OFFSET or \
            self.type == Type.CANNOT_COLOR
    @property
    def nasm(self):
        if self.type == Type.GLOBAL:
            return 'qword ' + '[' + GLOBAL_PREFIX + \
                self.name + ']'
        elif self.type == Type.OFFSET:
            return 'qword ' + '[' + self.reg.name + '+' \
                + str(self.offset) + ']'
        elif self.type == Type.REG:
            return reg.name
        else:
            return ''
