from abc import ABCMeta, abstract_method, abstract_property
from compiler.ast import ExprNode, Location
from compiler.ins.operand  import Reference
from compiler.type import Type
from compiler.utils import InternalError

class Entity(meta=ABCMeta):
    location = None
    name = None
    type = None
    offset = 0
    reference = None
    
    dependence = []
    is_output_irrelevant = False
    
    def __init__(self, loc, type, name):
        self.location = loc
        self.type = type
        self.name = name
        
    def add_dependence(self, entity):
        if  self != entity:
            dependence.append(entity)
    
