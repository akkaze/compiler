from compiler.entity.entity import Entity
from compiler.typ.string_type import StringType


class StringConstEntity(Entity):
    STRING_CONST_ASM_LABEL_PREFIX = 'STR_CONST_'

    def __init__(self, loc, type, name, expr):
        super().__init__(loc, type, StringType.STRING_CONST_PREFIX + name)
        self.expr = expr
        self.value = name
