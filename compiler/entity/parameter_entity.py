from compiler.entity import Entity 

class ParameterEntity(Entity):
    source = None
    def __init__(self, loc, type, name):
        super().__init__(loc, type, name)
