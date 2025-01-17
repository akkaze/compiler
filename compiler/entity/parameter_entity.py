from compiler.entity.entity import Entity


class ParameterEntity(Entity):

    def __init__(self, loc, type, name):
        super().__init__(loc, type, name)
        self.source = None
        self.func_entity = None
        self.arg_idx = 0

    def __str__(self):
        return str(self.func_entity) + ' {0}th arg : '.format(self.arg_idx) + str(self.name)
