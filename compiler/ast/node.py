from abc import ABC, abstractmethod, abstractproperty

class Node(ABC):
    def __init__(self):
        pass
    is_output_irrelevant = False
