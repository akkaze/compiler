from compiler.ast.expr_node import ExprNode

class LHSNode(ExprNode):
    def __init__(self):
        super().__init__()
        self.m_is_assignable = True
        self.m_type = None

    @property
    def alloc_size(self):
        return self.m_type.alloc_size()

    @property
    def is_lvalue(self):
        return True

    @property
    def type(self):
        return self.m_type

    @type.setter
    def type(self, value):
        self.m_type = value