from compiler.type import Type

class VoidType(Type):
    def __init__(self):
        super().__init__()

    @property
    def size(self):
        return 0
        
    @property
    def is_void(self):
        return True

    def is_compatible(self, other):
        return other.is_void

    def __str__(self):
        return 'void'
