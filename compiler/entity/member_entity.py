from compiler.entity.variable_entity import VariableEntity


class MemberEntity(VariableEntity):
    def __init__(self, entity):
        super().__init__(entity.location, entity.type,
                         entity.name, entity.initializer)
        self.entity = entity

    @property
    def type(self):
        return self.entity.type

    @property
    def size(self):
        return self.entity.size
