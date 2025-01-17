from abc import ABC, abstractmethod, abstractproperty

class Node(ABC):
    def __init__(self):
        self.is_output_irrelevant = False
        self.m_location = None

    @property
    def location(self):
        return self.m_location

    @location.setter
    def location(self, value):
        self.m_location = value