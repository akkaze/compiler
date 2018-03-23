class Immediate(Operand):
    class Type(Enum):
        LABEL = 1
        INTEGER = 2

    value = 0
    label = ''
    type = None
    
    def __init__(self, *args):
        if isinstance(args[0], int):
            self.value = args[0]
            self.type = Type.INTEGER
        else:
            self.label = args[0]
            self.type = Type.LABEL
    
    def __hash__(self):
        if self.type == Type.INTEGER:
            return value
        elif self.type == Type.LABEL:
            return hash(self.label)
        else:
            raise InternalError('invalid type of immediate')

    def __eq__(self, o):
        if isinstance(o, Immediate):
            if o.type == Type.LABEL:
                return self.type == o.label
            elif o.type == Type.INTEGER:
                return self.value == o.value
            else:
                raise InternalError('invalid type of immediate')
        return False

    def replace(self, from, to):
        return self

    @property
    def is_direct(self):
        return True
    @property
    def is_const_int(self):
        return self.type == Type.INTEGER
    def get_all_ref(self):
        return set()
    @property
    def nasm(self):
        if self.type == Type.INTEGER:
            return str(self.value)
        else:
            return label
    def __str__(self): 
        if self.type == Type.INTEGER:
            return str(self.value)
        else:
            return label
