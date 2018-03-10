from abc import {ABC, abstractmethod}

class Node(ABC):
    def __init__(self):
        pass
    is_output_irrelevant = False
    
    @abstractmethod
    def location(self):
        pass
