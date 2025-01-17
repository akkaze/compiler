from compiler.typ.typ import Type

class StringType(Type):
    STRING_CONST_PREFIX = '__string_constant'
    DEFAULT_SIZE = 8
    operator_and = None
    operator_eq = None
    operator_ne = None
    operator_lt = None
    operator_gt = None
    operator_ge = None
    operator_le = None
    scope = None

    @property
    def size(self):
        return self.DEFAULT_SIZE

    @property
    def is_string(self):
        return True

    def is_compatible(self, other):
        return other.is_string

    @property
    def is_full_comparable(self):
        return True

    @property
    def is_half_comparable(self):
        return True

    def __str__(self):
        return 'string'


