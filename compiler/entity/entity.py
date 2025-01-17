from abc import ABC, abstractmethod, abstractproperty


class Entity(ABC):
    def __init__(self, loc, type, name):
        self.location = loc
        self.m_type = type
        self.name = name
        self.dependence = set()
        self.offset = 0
        self.reference = None
        self.is_output_irrelevant = False
        self.m_asm_name = None
        self.m_size = 0

    def add_dependence(self, entity):
        if self != entity:
            self.dependence.add(entity)

    @property
    def asm_name(self):
        return self.m_asm_name

    @asm_name.setter
    def asm_name(self, value):
        self.m_asm_name = value

    @property
    def size(self):
        if self.m_size != 0:
            return self.m_size
        else:
            return self.type.size

    @size.setter
    def size(self, value):
        self.m_size = value

    @property
    def type(self):
        return self.m_type

    @type.setter
    def type(self, value):
        self.m_type = value