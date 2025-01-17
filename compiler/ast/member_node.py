from compiler.entity.entity import Entity
from compiler.ast.lhs_node import LHSNode
from compiler.ast.expr_node import ExprNode

class MemberNode(LHSNode):
    def __init__(self, expr, member):
        assert isinstance(expr, ExprNode)
        assert isinstance(member, str)
        self.expr = expr
        self.member = member
        self.entity = None
        super().__init__()

    @property
    def is_assignable(self):
        return not self.entity.type.is_function

    @property
    def location(self):
        return self.expr.location
    def accept(self, visitor):
        return visitor.visit(self)

    def __str__(self):
        mem_str = str(self.expr) + '.' +  self.member
        return mem_str