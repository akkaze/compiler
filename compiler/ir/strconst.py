from compiler.ir import Expr
from compiler.entity.string_const_entity import StringConstEntity

class StrConst(Expr):

    def __init__(self, entity):
        assert isinstance(entity, StringConstEntity)
        self.entity = entity
    def accept(self, emitter):
        return emitter.visit(self)
