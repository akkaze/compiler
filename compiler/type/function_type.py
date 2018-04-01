from compiler.type import Type

class FunctionType(Type):
    name = str()
    entity = None
    
    def __init__(self, name):
        self.name = name
    
    def size(self):
        raise InternalError('FunctionType#size called')
    @property
    def is_function(self):
        return True

    def is_compatible(self, other):
        if not other.is_function():
            return False
        return self.entity == other.entity

    def __str__(self):
        return 'function'
