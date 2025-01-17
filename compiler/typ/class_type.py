from compiler.typ.typ import Type


class ClassType(Type):
    CONSTRUCTOR_NAME = '__constructor__'
    DEFAULT_SIZE = 8

    def __init__(self, name):
        self.name = name
        self.entity = None

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
        return ClassType.DEFAULT_SIZE

    def __str__(self):
        return 'class ' + self.name 
