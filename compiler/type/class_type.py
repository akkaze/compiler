from compiler.type import Type

CONSTURCTOR_NAME = '__constructor__'

class ClassType(Type):
    DEFAULT_SIZE = 8
    name = ''
    entity = None
    def __init__(self, name):
        self.name = name

    @property
    def is_class(self):
        return True
    
    def is_compatible(self, other):
        if other.is_null:
            return True
        elif not other.is_class:
            return False
        return self.entity == other.entity

    @property
    def size(self):
        return self.DEFAULT_SIZE

    def __str__(self):
        return 'class ' + self.name 
