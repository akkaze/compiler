from abc import ABC. abstrctmethod, abstrctproperty
from compiler.ast import Node
from compiler.type import Type

class ExprNode(Node):
    is_assignable = False
    def __init__(self):
        super().__init__()

    @abstrctproperty
    def alloc_size(self):
        return self.type.alloc_size

    @abstrctproperty
    def is_constant(self):
        return False

    @abstrctproperty
    def is_parameter(self):
        return False

    @abstrctproperty
    def is_lvalue(self):
        return False

    @abstrctproperty
    def is_assignable(self):
        return self.is_assignable
    
    @abstrctproperty
    def is_loadable(self):
        return False


