from compiler.entity import Entity
from compiler.ast import LHSNode

class MemberNode(LHSNode):
    expr = None
    member = ''
    entity = None
    def __init__(self, expr, member):
        self.expr = expr
        self.member = member
        super().__init__()

    @property
    def is_assignable(self):
        return not entity.type.is_function

    @property
    def location(self):
        return expr.location
    def accept(self, visitor):
        return visitor.visit(self)
