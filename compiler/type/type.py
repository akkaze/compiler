from abc import ABC, abstractproperty, abstractmethod

class Type(ABC):
    @property
    def is_void(self):
        return False
    @property
    def is_bool(self):
        return False
    @property
    def is_integer(self):
        return False
    @property
    def is_string(self):
        return False
    @property
    def is_array(self):
        return False
    @property
    def is_class(self):
        return False
    @property
    def is_function(self):
        return False
    @property
    def is_null():
        return False
    @property
    def is_full_comparable(self):
        return False
    @property
    def is_half_comparable(self):
        return False
    @abstractmethod
    def is_compatible(self, other):
        pass
    @abstractproperty
    def size(self):
        pass
    def alloc_size(self):
        return self.size()
