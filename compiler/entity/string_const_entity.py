from compiler.entity import Entity
from compiler.type import STRING_CONSTANT_PREFIX
class StringConstantEntity(Entity):
    expr = None
    value = ''
    asm_name = ''
    STRING_CONST_ASM_LABEL_PREFIX = 'STR_CONST_'

    def __init__(self, loc, type, name, expr):
        super().__init__(loc, type, name, STRING_CONST_PREFIX + name)
        self.expr = expr
        self.value = name
    







