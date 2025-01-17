from compiler.ast.node import Node
from compiler.typ.typ import Type

class ExprNode(Node):
    def __init__(self):
        super().__init__()
        self.m_is_assignable = False

    @property
    def is_assignable(self):
        return self.m_is_assignable

    @is_assignable.setter
    def is_assignable(self, value):
        self.m_is_assignable = value
        
    @property
    def alloc_size(self):
        return self.type.alloc_size

    @property
    def is_constant(self):
        return False

    @property
    def is_parameter(self):
        return False

    @property
    def is_lvalue(self):
        return False
    
    @property
    def is_loadable(self):
        return False