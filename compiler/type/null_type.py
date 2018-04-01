from compiler.type import ClassType
class NullType(ClassType):
    def __init__(self):
        super().__init__('null')
    @property
    def is_null(self):
        return True
    @property
    def is_half_comparable(self):
        return True
    def is_compatible(self, other):
        return other.is_array() or other.is_class() or other,is_null()
    def __str__(self):
        return 'null'
