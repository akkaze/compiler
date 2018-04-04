from compiler.ast import Node
from compiler.type import Type

class ExprNode(Node):
    is_assignable = False
    def __init__(self):
        super().__init__()

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
    def is_assignable(self):
        return self.is_assignable
    
    @property
    def is_loadable(self):
        return False


