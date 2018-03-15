import compiler.entity import VariableEntity

class MemberEntity(VariableEntity):
    def __init__(self, entity):
        super().__init__(entity.location, entity.type \
                        entity.name, entity.initializer)
