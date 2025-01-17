from compiler.typ.typ import Type

class BoolType(Type):
    DEFAULT_SIZE = 8
    @property
    def is_bool(self):
        return True
    def is_compatible(self, other):
        return other.is_bool
    @property
    def is_half_comparable(self):
        return True
    @property
    def size(self):
        return self.DEFAULT_SIZE
    def __str__(self):
        return 'bool'
