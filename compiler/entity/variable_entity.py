from compiler.entity import Entity

class VariableEntity(Entity):
    initializer = None
    
    def __init__(self, loc, type, name, init):
        super().__init__(loc, type, name)
        self.initializer = init

    def __str__(self):
        return 'variable entity : ' + self.name
