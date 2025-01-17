from compiler.entity.entity import Entity

class VariableEntity(Entity):    
    def __init__(self, loc, type, name, init):
        super().__init__(loc, type, name)
        self.initializer = init

    def __deep_copy__(self, memo):
       new_var = VariableEntity(self.location, self.type, self.name, self.initializer)
       new_var.is_output_irrelevant = False
       return new_var

    def __str__(self):
        return 'variable entity : ' + self.name
