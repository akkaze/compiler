from complier.ast import ExprNode, Location
from complier.type import Type
from compiler.entity.entity import *

class VariableEntity(Entity):
    initializer = None
    
    def __init__(self, loc, type, name, init):
        super(VariableEntity, self).__init__(loc, type, name, init)
        self.initializer = init
    
    def initializer(self):
        return self.initializer
