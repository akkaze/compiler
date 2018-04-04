from abc import ABC, abstractmethod, abstractproperty

class Entity(ABC):
    location = None
    name = None
    type = None
    offset = 0
    reference = None
    
    dependence = None
    is_output_irrelevant = False
    
    def __init__(self, loc, type, name):
        self.location = loc
        self.type = type
        self.name = name
        self.dependence = []

    def add_dependence(self, entity):
        if  self != entity:
            self.dependence.append(entity)

    @property
    def value(self):
        raise InternalError('Entity#value called')
    
    @property
    def size(self):
        return self.type.size    
