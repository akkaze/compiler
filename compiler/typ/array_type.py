from compiler.typ.typ import Type
from compiler.utils.libfunction import LibFunction


class ArrayType(Type):
    DEFAULT_POINTER_SIZE = 8

    magic_array = None
    scope = None
    def __init__(self, base_type, dimension=0):
        if dimension == 0:
            self.base_type = base_type
        elif dimension == 1:
            self.base_type = base_type
        else:
            self.base_type = ArrayType(base_type, dimension - 1)

    @property
    def deep_type(self):
        if isinstance(self.base_type, ArrayType):
            return self.base_type.deep_type
        else:
            return self.base_type

    @property
    def is_array(self):
        return True

    @property
    def is_half_comparable(self):
        return True

    @property
    def size(self):
        return ArrayType.DEFAULT_POINTER_SIZE

    def is_compatible(self, other):
        if other.is_null:
            return True
        elif not other.is_array:
            return False
        return self.base_type.is_compatible(other.base_type)

    def __str__(self):
        return str(self.base_type) + '[]'
