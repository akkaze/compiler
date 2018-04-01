from compiler.type import Type
class IntegerType(Type):
    DEFAULT_SIZE = 8
    @property
    def is_integer(self):
        return True
    def is_compatible(self, other):
        return other.is_integer
    @property
    def is_full_comparable(self):
        return True
    @property
    def is_half_comparable(self):
        return True
    @property
    def size(self):
        return self.DEFAULT_SIZE
    def __str__(self):
        return 'int'
