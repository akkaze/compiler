from compiler.ast import ExprNode
from compiler.type import Type

class LHSNode(ExprNode):
    type = None

    def __init__(self):
        super().__init__()

    @property
    def alloc_size(self):
        return self.type.alloc_size()

    @property
    def is_lvalue(self):
        return True

    @property
    def is_assignable(self):
        return True

